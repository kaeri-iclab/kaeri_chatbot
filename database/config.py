import os
from dotenv import load_dotenv
import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Load environment variables
load_dotenv("/home/h2002a/kaeri_chatbot/kkaeri/.env", override=True)
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class Settings(BaseSettings):
    backend_db: str = os.getenv("BACKEND_DB", "")
    db_pool_size: int = 20
    db_max_overflow: int = 10
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    SEARCH_ENGINE_ID: str = os.getenv("SEARCH_ENGINE_ID", "")
    MILVUS_URI: str = os.getenv("MILVUS_URI", "")
    MILVUS_TOKEN: str = os.getenv("MILVUS_TOKEN", "")
    langchain_api_key: Optional[str] = None

    model_config = SettingsConfigDict(
#        env_file="/home/h2002a/kaeri_chatbot/kkaeri.env",
        env_file ="~/kaeri_chatbot/.env",
        extra="allow",
        case_sensitive=False,
    )


# Set LangChain environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "padong"

settings = Settings()

# Print settings for debugging
print("Loaded settings:")
for key, value in settings.model_dump().items():
    print(f"{key}: {value}")
