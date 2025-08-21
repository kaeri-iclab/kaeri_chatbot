from sqlalchemy.orm import Session
from models import UserQuery

def save_answer(db: Session, user_id: str, utterance: str, response: str):

    user_query = UserQuery(
        user_id = user_id,
        utterance = utterance,
        response = response)


    db.add(user_query)
    db.commit()
    db.refresh(user_query)

    return user_query
