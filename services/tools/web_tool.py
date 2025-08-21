# ───────────── tools/web_search_tool.py ─────────────
import os, logging
from dotenv import load_dotenv
from typing import Annotated

from openai import AsyncOpenAI
from langchain.tools import tool

# ── 환경 변수 및 로깅 ──────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── OpenAI Async 클라이언트 ───────────────────────────
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# ── 실제 호출 로직 ─────────────────────────────────────
async def _call_web_search_preview(query: str) -> str:
    """
    OpenAI Responses API의 web_search_preview 툴을 호출해
    검색 결과를 요약한 텍스트를 반환합니다.
    """
    resp = await client.responses.create(
        model="gpt-4o",
        input=query,
        instructions="Please organize and provide the web search results.",
        tools=[{"type": "web_search_preview"}],
    )
    logger.info("🛰️  web_search_preview 응답 길이: %d", len(resp.output_text))
    return resp.output_text


# ── @tool: Docstring + Annotated 방식 ──────────────────
@tool  # name·description 인자 없이 → 함수 이름 & Docstring 사용
async def web_search_tool(
    query: Annotated[str, "웹에서 검색할 질문 또는 키워드"],
) -> Annotated[str, "웹 검색 요약 결과"]:
    """Use web_search ONLY IF the user's question clearly does not fall within responses_api, vectorstore, or general categories, such as:
   - 일반 상식, 날씨, 뉴스, 실시간 정보 등."""
    return await _call_web_search_preview(query)
# ──────────────────────────────────────────────────────
