from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from pymilvus import connections, utility, Collection
import os
import pandas as pd
from langchain_core.documents import Document
from tqdm import tqdm
import uuid
from database.dependencies import get_db
from database.models import Setting
from PyPDF2 import PdfReader
from fastapi import FastAPI, File, UploadFile
import logging
from database import orm

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

orm.Base.metadata.create_all(bind=orm.engine)


# Load environment variables
milvus_host = os.getenv("MILVUS_HOST", "standalone")
milvus_port = os.getenv("MILVUS_PORT", "19530")
collection_name = "nuclear_topics"
# Connect to Milvus server
connections.connect(host=milvus_host, port=milvus_port)

collection_name = "nuclear_topics"
connections.connect(host="standalone", port="19530")


# Load CSV data and create documents
def get_documents():
    csv_file_path = "chunked_nuclear_safety_data.csv"
    df = pd.read_csv(csv_file_path)
    documents = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing documents"):
        content = row["content"]
        title = row["title"]

        # content가 문자열이 아닌 경우 처리
        if not isinstance(content, str):
            content = str(content)  # 문자열로 변환

            for i, split_content in enumerate(content):
                id = uuid.uuid4().hex
                doc = Document(
                    page_content=split_content,
                    metadata={
                        "title": f"{title} (Part {i + 1})",
                        "content_id": id + "_" + str(i),
                    },
                )
                documents.append(doc)
        else:
            doc = Document(
                page_content=content,
                metadata={
                    "title": title,
                    "content_id": uuid.uuid4().hex,
                },
            )
            documents.append(doc)

    return documents


# pdf 처리 함수
def process_pdf(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    pdf_documents = []
    for page_number, page in enumerate(reader.pages, start=1):
        content = page.extract_text()
        doc = Document(
            page_content=content,
            metadata={
                "title": f"{os.path.basename(pdf_file_path)} - Page {page_number}"
            },
        )
        pdf_documents.append(doc)
    return pdf_documents


def initialize_vector_store(force_reload=False):
    openai_api_key = next(get_db()).query(Setting).first().key
    if openai_api_key is None:
        print("OpenAI API key is not set. Please set the key in the settings.")
        return

    documents = get_documents()
    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key, model="text-embedding-ada-002"
    )

    if utility.has_collection(collection_name) and not force_reload:
        print(f"Collection '{collection_name}' already exists.")
        collection = Collection(collection_name)
        print(f"Number of entities in the collection: {collection.num_entities}")
        if collection.num_entities > 0:
            print("Collection already has data. Skipping insertion.")
            vector_store = Milvus(
                collection_name=collection_name,
                embedding_function=embeddings,
                connection_args={"host": "standalone", "port": "19530"},
                text_field="content",
                vector_field="vector",
                primary_field="id",
            )
        else:
            print("Collection is empty. Inserting data.")
            utility.drop_collection(collection_name)
            vector_store = create_vector_store(documents, embeddings)
    else:
        if force_reload and utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f"Collection '{collection_name}' deleted.")
        print(f"Creating and populating collection '{collection_name}'.")
        vector_store = create_vector_store(documents, embeddings)

    # 인덱스 재생성
    collection = Collection(collection_name)
    collection.release()
    collection.drop_index()
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
    }
    collection.create_index(field_name="vector", index_params=index_params)
    collection.load()

    print(f"Total documents after processing: {collection.num_entities}")
    print("Vector store initialization done.")
    return vector_store


def create_vector_store(documents, embeddings):
    return Milvus.from_documents(
        documents,
        embeddings,
        collection_name=collection_name,
        connection_args={"host": "standalone", "port": "19530"},
        index_params={"metric_type": "L2"},
        text_field="content",
        vector_field="vector",
        primary_field="id",
        consistency_level="Strong",
        drop_old=True,
    )


# 초기 설정


app = FastAPI()


