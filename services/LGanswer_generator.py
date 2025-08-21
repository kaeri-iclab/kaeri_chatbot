from sqlalchemy.orm import Session
from routers.langgraph_router import run_graph, research_app
import logging, httpx
from langchain_core.messages import BaseMessage, AIMessage
from openai import AsyncOpenAI
from database.dependencies import get_db
from database.models import Setting
import asyncio


logger = logging.getLogger(__name__)


def _pick_final_answer(messages: list[BaseMessage]) -> str | None:
    for m in reversed(messages):
        if isinstance(m, AIMessage) and getattr(m, "content", None):
            return m.content
    return None

# 1) 그래프 기반 텍스트 답변 생성 함수
async def generate_answer_via_graph(utterance: str, user_id: str):
    output = await run_graph(research_app, utterance, user_id)
    if output and isinstance(output, dict):
        messages = output.get("messages", []) or []
        ai_text = _pick_final_answer(messages)

        # 에코방지
        if ai_text and utterance and ai_text.strip() == utterance.strip():
            ai_text = "방금 말씀하신 내용을 확인했어요. 어떤 점이 더 궁금하신가요? 🙂"

        if ai_text:
            return ai_text[:800]

    logger.error("유효한 최종 상태를 받지 못했습니다. State: %s", output)
    return "답변을 생성하는 데 실패했습니다. 다시 시도해주세요."


async def LGsend_callback(answer_text: str, callback_url: str):
    """
    생성된 답변을 카카오톡의 callbackUrl로 전송하는 함수
    """
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer_text
                    }
                }
            ]
        }
    }

    try:
        # 비동기 HTTP 클라이언트를 사용해 POST 요청을 보냅니다.
        async with httpx.AsyncClient() as client:
            response = await client.post(callback_url, json=payload, timeout=5)
            response.raise_for_status()  # 2xx 응답이 아니면 예외를 발생시킵니다.
        logger.info(f"Callback to {callback_url} successful, response: {response.text}")
    except httpx.RequestError as e:
        logger.error(f"Failed to send callback to {callback_url}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during callback: {e}")



openai_api_key = next(get_db()).query(Setting).first().key

# 2) 이미지 답변 함수
async def generate_answer_image(utterance: str, image_url: str, db:Session, user_id: str):
    client = AsyncOpenAI(api_key=openai_api_key)
    logger.info(f"이미지 답변 함수에서 보는 image_url은 {image_url}")

    # 요청할 메시지 구성
    response = await client.responses.create(
        model="gpt-4o",
        input=[
        {
            "role": "user",
            "content": [
                {"type":"input_text","text":utterance},
                {"type":"input_image","image_url": image_url}
            ]
        }
    ]
)
    logger.info(f"assistant 답변: {response}")
    answers = response.output_text



    return answers



# 3) BackgroundTasks 에 예약할 함수 (이게 FastAPI 코드에서 호출됩니다)
async def LGgenerate_and_send_answer(utterance: str, user_id: str, callback_url: str, db: Session, image_url: str = None):
    logger.info(f"✅ [LG 백그라운드 시작] user: {user_id}, utterance: {utterance}")
    try:
        answer = None # 답변 변수 초기화

        if image_url is None:
            logger.info("➡️ [LG] 텍스트 답변 생성을 시작합니다...")
            answer = await generate_answer_via_graph(utterance, user_id) 
            logger.info(f"⬅️ [LG] 텍스트 답변 생성 완료: {answer}")
        else:
            logger.info("➡️ [LG] 이미지 답변 생성을 시작합니다...")
            answer = await generate_answer_image(utterance, image_url, db, user_id)
            logger.info(f"⬅️ [LG] 이미지 답변 생성 완료: {answer}")

        if answer:
            logger.info(f"🚀 [LG] 콜백 전송을 시작합니다. URL: {callback_url}")
            await LGsend_callback(answer, callback_url)
            logger.info("✅ [LG 백그라운드 성공] 콜백 전송 완료.")
        else:
            logger.error("❗️ [LG] 답변이 생성되지 않았습니다 (결과가 None 또는 비어있음).")
            await LGsend_callback("죄송합니다, 답변을 생성하지 못했습니다.", callback_url)

    except Exception as e:
        logger.critical(f"🔥 [LG 백그라운드 오류] 작업 중 예외 발생: {e}", exc_info=True)
        error_message = "죄송합니다. 답변을 처리하는 중 오류가 발생했습니다."
        await LGsend_callback(error_message, callback_url)
