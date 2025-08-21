from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.dependencies import get_db
from database.models import Conversation
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/conversation")
def get_conversation_count(duration: str, db: Session = Depends(get_db)):
    current_time = datetime.now()

    if duration == "day":
        start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    elif duration == "week":
        start_time = current_time.replace(
            day=current_time.day - current_time.weekday() - 2
        )
    elif duration == "month":
        start_time = current_time.replace(
            month=current_time.month - 1, day=current_time.day
        )
    elif duration == "year":
        start_time = current_time.replace(
            year=current_time.year - 1, month=current_time.month, day=current_time.day
        )
    else:
        return {"error": "Invalid duration. Use 'day', 'week', 'month', or 'year'."}

    if duration == "day":
        query = (
            db.query(
                func.date_trunc("hour", Conversation.timestamp).label("date"),
                func.count(Conversation.id).label("count"),
            )
            .group_by(func.date_trunc("hour", Conversation.timestamp))
            .filter(Conversation.timestamp >= start_time)
            .all()
        )
    else:
        query = (
            db.query(
                func.date(Conversation.timestamp).label("date"),
                func.count(Conversation.id).label("count"),
            )
            .group_by(func.date(Conversation.timestamp))
            .filter(Conversation.timestamp >= start_time)
            .all()
        )

    if duration == "day":
        res = [
            {"date": hour.strftime("%Y-%m-%d %H:00:00"), "count": count}
            for hour, count in query
        ]
        while start_time < current_time:
            start_time += timedelta(hours=1)
            if not any(
                d["date"] == start_time.strftime("%Y-%m-%d %H:00:00") for d in res
            ):
                res.append(
                    {"date": start_time.strftime("%Y-%m-%d %H:00:00"), "count": 0}
                )
        res.sort(key=lambda x: x["date"])
    else:
        res = [
            {"date": date.strftime("%Y-%m-%d"), "count": count} for date, count in query
        ]
        while start_time < current_time:
            start_time += timedelta(days=1)
            if not any(d["date"] == start_time.strftime("%Y-%m-%d") for d in res):
                res.append({"date": start_time.strftime("%Y-%m-%d"), "count": 0})
        res.sort(key=lambda x: x["date"])

    return res


@router.get("/query_type")
def get_query_type(duration: str, db: Session = Depends(get_db)):
    current_time = datetime.now()

    if duration == "day":
        start_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    elif duration == "week":
        start_time = current_time.replace(
            day=current_time.day - current_time.weekday()
        ).replace(hour=0, minute=0, second=0, microsecond=0)
    elif duration == "month":
        start_time = current_time.replace(
            month=current_time.month - 1, day=current_time.day
        )
    elif duration == "year":
        start_time = current_time.replace(
            year=current_time.year - 1, month=current_time.month, day=current_time.day
        )
    else:
        return {"error": "Invalid duration. Use 'day', 'week', 'month', or 'year'."}

    query = (
        db.query(Conversation.type, func.count(Conversation.id).label("count"))
        .group_by(Conversation.type)
        .filter(Conversation.timestamp >= start_time)
        .order_by(func.count(Conversation.id).desc())
        .limit(5)
        .all()
    )

    return [{"type": qtype, "count": count} for qtype, count in query]
