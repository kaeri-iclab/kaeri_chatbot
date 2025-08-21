from fastapi import APIRouter, File, UploadFile, HTTPException
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_milvus import Milvus
import pymupdf
from database.dependencies import get_db
from pymilvus import MilvusClient, Collection, utility
import uuid
from database.models import Setting
from services.vector_store import (
    get_documents,
    create_vector_store,
)  # csv 파일 자동로드를 위함

router = APIRouter()
collection_name = "nuclear_topics"
client = MilvusClient(
    uri="http://standalone:19530"
)


@router.get("/")
def get_list(page: int = 1):
    openai_api_key = next(get_db()).query(Setting).first().key
    if openai_api_key is None:
        raise HTTPException(status_code=400, detail="OpenAI API key를 등록해주세요.")
    if utility.has_collection(collection_name) is False:
        raise HTTPException(status_code=400, detail="Collection이 존재하지 않습니다.")
    collection = Collection(collection_name)
    collection.load()
    res = client.query(
        collection_name=collection_name,
        filter="",
        limit=20,
        offset=(page - 1) * 20,
        output_fields=["*"],
    )

    return {
        "collection": [
            {"title": doc["title"], "content": doc["content"], "id": doc["content_id"]}
            for doc in res
        ],
        "num": collection.num_entities,
    }


@router.post("/upload")
async def upload_pdf(files: list[UploadFile] = File(...)):
    openai_api_key = next(get_db()).query(Setting).first().key
    docs = []

    csv_documents = get_documents()
    docs.extend(csv_documents)
    for file in files:
        stream = await file.read()
        pdf = pymupdf.open(stream=stream)
        id = uuid.uuid4().hex
        for i, page in enumerate(pdf):
            content = page.get_text()
            doc = Document(
                page_content=content,
                metadata={
                    "title": f"{file.filename} (Part {i + 1})",
                    "content_id": id + "_" + str(i),
                },
            )
            docs.append(doc)

    if openai_api_key is None:
        raise HTTPException(status_code=400, detail="OpenAI API key를 등록해주세요.")
    if utility.has_collection(collection_name) is False:
        raise HTTPException(status_code=400, detail="Collection이 존재하지 않습니다.")

    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key, model="text-embedding-ada-002"
    )
    vector_store = Milvus(
        embeddings,
        collection_name=collection_name,
        connection_args={"host": "standalone", "port": "19530"},
        index_params={"metric_type": "L2"},
        text_field="content",
        vector_field="vector",
        primary_field="id",
        consistency_level="Strong",
        drop_old=True,
        auto_id=True,
    )
    vector_store.add_documents(docs)
    # documents = get_documents() #csv 파일 자동로드를 위함
    # create_vector_store(documents) #csv 파일 자동로드를 위함
    print(f"Added {len(docs)} documents to Milvus collection {collection_name}")
    collection = Collection(collection_name)
    collection.flush()

    return {"message": "PDF uploaded successfully"}
