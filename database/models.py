from database.orm import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime



class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    input = Column(String)
    output = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    type = Column(String, nullable=False, default="")


class FAQ(Base):
    __tablename__ = "faq"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)


class Setting(Base):
    __tablename__ = "setting"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=True)
    query_model = Column(String, nullable=False, default="gpt-4o-mini")
    ai_model = Column(String, nullable=False, default="gpt-4o-mini")


class UserQuery(Base):

    __tablename__ = "user_queries"


    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(String, index = True)
    utterance = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default = datetime.utcnow)
    response_id = Column(String, nullable=True)
