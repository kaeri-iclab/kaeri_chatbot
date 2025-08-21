from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.dependencies import get_db
from sqlalchemy.orm import Session
from database.models import FAQ

router = APIRouter()


class FAQInput(BaseModel):
    question: str
    answer: str


class DeleteFAQInput(BaseModel):
    ids: list[str]


@router.get("/")
def get_faq(db: Session = Depends(get_db)):
    faqs = db.query(FAQ).all()
    return faqs


@router.post("/")
async def add_faq(input: FAQInput, db: Session = Depends(get_db)):
    new_faq = FAQ(question=input.question, answer=input.answer)
    db.add(new_faq)
    db.commit()
    return new_faq


@router.delete("/")
async def delete_faq(input: DeleteFAQInput, db: Session = Depends(get_db)):
    for id in input.ids:
        db.query(FAQ).filter(FAQ.id == id).delete()
    db.commit()
    return {"message": "FAQs deleted successfully!"}
