from database.orm import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def get_db():
    with SessionLocal() as db:
        try:
            yield db
            db.commit()
            logger.info(f"db 출력: {db}")
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error occurred")
            raise
        except Exception as e:
            db.rollback()
            logger.critical(f"Unexpected error occurred")
            raise
