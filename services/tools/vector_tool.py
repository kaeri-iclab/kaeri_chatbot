from typing import List, Optional
from langchain_core.tools.base import BaseTool, ToolException
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_milvus import Milvus

from database.orm import SessionLocal
from database.models import Setting
import asyncio


# ────────────────────────────────────────────────
# 1. TavilySearch 스타일의 Tool 클래스
# ────────────────────────────────────────────────
class MilvusSearchTool(BaseTool):
    """
    Milvus 벡터 DB에서 유사도 검색을 수행해
    LangChain Document 리스트를 반환하는 Tool.
    """
    name: str = "MilvusVectorSearch"
    description: str = (
        "Use this tool for all questions related to external, academic, and technical knowledge about the field of nuclear energy. "
        "Good for topics like: Nuclear technology principles, SMRs, nuclear fusion, radiation safety, research trends, government policies, and scientific papers."
    )

    # 사용자 지정 파라미터
    k: int = 4                           # 가져올 문서 개수
    nprobe: int = 10                     # Milvus 검색 파라미터
    char_limit: Optional[int] = 500      # 문서 길이 제한(없으면 None)
    collection_name: str = "nuclear_topics"
    milvus_host: str = "standalone"
    milvus_port: int = 19530



    # ── 동기 실행 함수 (필수) ───────────────────────
    def _run(self, query: str, **kwargs) -> List[Document]:
        # ① 세션 열기
        with SessionLocal() as db:
            setting = db.query(Setting).first()
            if not setting:
                raise ToolException("Setting row not found")
            api_key = setting.key
        # ② Embedding & Milvus 인스턴스
        embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model="text-embedding-ada-002"
        )
        vec_store = Milvus(
            embeddings,
            collection_name=self.collection_name,
            connection_args={"host": self.milvus_host,
                             "port": str(self.milvus_port)},
            index_params={"metric_type": "L2"},
            text_field="content",
            vector_field="vector",
            primary_field="id",
            consistency_level="Strong",
        )
        # ③ 검색
        docs = vec_store.similarity_search(
            query,
            k=self.k,
            search_params={"metric_type": "L2",
                           "params": {"nprobe": self.nprobe}}
        )
        if self.char_limit:
            for d in docs:
                d.page_content = d.page_content[: self.char_limit]
        return docs

    # 비동기
    async def _arun(self, query: str, **kwargs):
        return await asyncio.to_thread(self._run, query)
