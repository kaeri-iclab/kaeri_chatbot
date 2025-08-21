from fastapi import APIRouter, FastAPI, Request, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from database.dependencies import get_db
import logging
import asyncio
from services.LGanswer_generator import generate_answer_via_graph, LGgenerate_and_send_answer
from database.save_answer import save_answer
import httpx
from PIL import Image
import io


logger = logging.getLogger(__name__)

# APIRouter 객체 생성
router = APIRouter()
app = FastAPI(
    title="KakaoTalk GPT Chatbot",
    version="1.0",
    description="A KakaoTalk bot using FastAPI, LangChain's OpenAI model, and Milvus for RAG",
)

user_image_store = {}


@router.post("/callback")
async def kakao_callback(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    body = await request.json()
    logger.info(f"Received request body: {body}")

    user_request = body.get('userRequest', {})
    user = user_request.get('user', {})
    
    utterance = user_request.get('utterance')
    user_id = user.get('id')
    callback_url = user_request.get('callbackUrl')
    image_url = user_request.get("params",{}).get("media", {}).get('url')
    
    # 카카오톡 채널 추가 여부 등 추가 정보도 여기서 파싱 가능
    # is_friend = user.get('properties', {}).get('isFriend', False)

    logger.info(f"Extracted fields - utterance: {utterance}, user_id: {user_id}, callback_url: {callback_url}, image_url: {image_url}")

    # 필수 정보 확인
    if not all([utterance, user_id, callback_url]):
        logger.error("Required fields are missing in the request")
        # 이 경우는 콜백을 사용할 수 없으므로 직접 에러 메시지를 반환합니다.
        return {"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "요청 정보가 부족합니다."}}]}}

    # 1. 이미지 처리 로직
    image_url_from_request = body.get("userRequest", {}).get("params", {}).get("media", {}).get('url')
    
    # 사용자가 이미지를 새로 올렸을 때
    if image_url_from_request:
        # 사용자의 이전 이미지는 삭제하고 새로 저장
        user_image_store[user_id] = image_url_from_request
        logger.info(f"Image URL for user {user_id} saved: {image_url_from_request}")
        # 이미지 업로드 후에는 질문을 유도하는 빠른 응답을 보냄
        return {
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": "사진을 잘 받았어요! 어떤 점이 궁금하신가요?"}}]
            }
        }

    # 2. 답변 생성 로직 (항상 백그라운드 실행)
    
    # 이전에 저장된 이미지가 있는지 확인
    image_to_process = user_image_store.get(user_id)
    
    # 백그라운드 작업 등록
    background_tasks.add_task(
        LGgenerate_and_send_answer,
        utterance=utterance,
        user_id=user_id,
        callback_url=callback_url,
        db=db,
        image_url=image_to_process
    )
    
    # 답변 생성 후에는 저장된 이미지 정보 삭제 (선택적)
    if image_to_process:
        user_image_store.pop(user_id, None) # 해당 유저의 이미지 정보만 안전하게 삭제
        logger.info(f"Image URL for user {user_id} will be processed and removed.")

    # DB에 질문 저장 (빠른 응답)
    save_answer(db, user_id, utterance, "생각 중 ..")

    # 3. 카카오톡 서버에 "처리 중" 신호 전송
    # 항상 useCallback: True를 반환하여 사용자 경험을 일관되게 만듭니다.
    return {
        "version": "2.0",
        "useCallback": True,
        "data": {
            # 이 data 필드는 사용자에게 보이진 않지만, 로깅/디버깅 용도로 활용할 수 있습니다.
            "message": "Processing user request in background"
        }
    }
