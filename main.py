from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import kakao, dashboard, vectordb, faq, settings
import os
from database import orm
from dotenv import load_dotenv

load_dotenv()
orm.Base.metadata.create_all(bind=orm.engine)
admin_address = os.getenv("ADMIN_PAGE_ADDRESS", "localhost")
host = os.getenv("API_HOST", "localhost")

# IP 화이트리스트를 .env 파일에서 가져옵니다
WHITELIST_IPS = os.getenv("WHITELIST_IPS", "127.0.0.1").split(",")

app = FastAPI(
    title="KakaoTalk GPT Chatbot",
    version="1.0",
    description="A KakaoTalk bot using FastAPI, LangChain's OpenAI model, and Milvus for RAG",
)

# IP 화이트리스트 미들웨어
@app.middleware("http")
async def ip_whitelist_middleware(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in WHITELIST_IPS:
        return JSONResponse(status_code=403, content={"message": "Access denied"})
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[admin_address],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kakao.router)
app.include_router(dashboard.router, prefix="/dashboard")
app.include_router(vectordb.router, prefix="/db")
app.include_router(faq.router, prefix="/faq")
app.include_router(settings.router, prefix="/setting")


@app.get("/")
async def root():
    return {"message": "생각 중 ... "}

if __name__ == "__main__":
    import uvicorn

    load_dotenv()

    host = os.getenv("HOST", host)  # 기본값으로 localhost 사용

    uvicorn.run(
        "main:app",
        host=host,
        port=int(os.getenv("PORT", 8077)),
        reload=True,
        reload_excludes="admin",
    )
