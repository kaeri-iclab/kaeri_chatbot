# ───────────── tools/api_tool.py ─────────────
import os, asyncio
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI

from pydantic import BaseModel, Field
from typing import Annotated
from langchain.tools import tool            # 데코레이터 방식
# --------------------------------------------

load_dotenv()
client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

VS_ID = os.environ["VECTOR_STORE_ID"]        # .env에 등록해 둔 벡터스토어 ID

PROMPT_PATH = Path(__file__).parent / "prompt.txt"
SYS_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")


async def _kaeri_rag_call(query: str) -> str:
    """OpenAI Responses API + KAERI 벡터스토어 호출 로직"""
    resp = await client.responses.create(
        model="gpt-4o",
        input=query,
        instructions=SYS_PROMPT,
        tools=[{"type": "file_search", "vector_store_ids": [VS_ID]}],
    )
    return resp.output_text


# --------- 툴 정의 (Docstring & Annotated) ----------
class SearchArgs(BaseModel):
    query: str = Field(..., description="KAERI 내부 규정·지침 검색 질의")

@tool                                   # name/description 인자 없이!
async def kaeri_internal_search(
    query: Annotated[str, "KAERI 내부 규정·지침 검색 질의"],
) -> Annotated[str, "규정 요약 답변"]:
    """Use responses_api for detailed internal guidelines, regulations, management rules, and procedures specifically related to the Korea Atomic Energy Research Institute (KAERI), including:
    - 감사, 회계, 인사관리, 연구기술, 자재시설, 조직, 총무, 정관, 직제, 원규관리, 위원회 관련 내부규정 및 지침 내용.
    Please return all reference materials along with your response. (EX: (참고자료: [감사] 외부강의등 사례금 상한액 - 별표 2).)"""
    return await _kaeri_rag_call(query)
# ----------------------------------------------------
