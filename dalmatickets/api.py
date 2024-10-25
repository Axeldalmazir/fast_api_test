"""
api.py
---

The REST Api for the Globoticket events database.
"""
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from dalmatickets.crud import get_all_dbevents, get_dbevent
from dalmatickets.database import SessionLocal
from dalmatickets.models import DBEvent
from dalmatickets.schemas import Event

app = FastAPI()

PROJECT_ROOT = Path(__file__).parent.parent


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/event/{id}", response_model=Event)
def get_event(id: int, db: Annotated[Session, Depends(get_session)]) -> DBEvent:
    """Retrieve a single event by id. Returns status 404 if event is not found."""
    event = get_dbevent(id, db)
    if event is None:
        raise HTTPException(status_code=404, detail=f"No product with id {id}")
    return event


@app.get("/event/", response_model=list[Event])
def get_all_events(db: Annotated[Session, Depends(get_session)]) -> list[DBEvent]:
    return get_all_dbevents(db)


# This should come AFTER all other endpoints
app.mount("/", StaticFiles(directory=PROJECT_ROOT / "static", html=True))
