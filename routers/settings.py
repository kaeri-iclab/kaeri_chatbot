from fastapi import APIRouter, Depends
from database.dependencies import get_db
from sqlalchemy.orm import Session
from database.models import Setting
from pydantic import BaseModel
from services.vector_store import initialize_vector_store

router = APIRouter()


class SettingInput(BaseModel):
    key: str
    query_model: str
    ai_model: str


@router.get("/")
async def get_setting(db: Session = Depends(get_db)):
    setting = db.query(Setting).first()
    return setting


@router.put("/")
def change_key(input: SettingInput, db: Session = Depends(get_db)):
    setting = db.query(Setting).first()

    setting.key = input.key

    setting.query_model = input.query_model
    setting.ai_model = input.ai_model
    db.commit()

    initialize_vector_store(force_reload=True)
    return setting
