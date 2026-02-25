from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SecurityEvent, Server, SecurityPolicy
from schemas import EventCreate, EventRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EventRead)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == event.server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    policy = db.query(SecurityPolicy).filter(SecurityPolicy.id == event.policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    db_event = SecurityEvent(
        server_id=event.server_id,
        policy_id=event.policy_id,
        event_type=event.event_type,
        severity=event.severity,
        description=event.description
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)):
    return db.query(SecurityEvent).all()

@router.get("/server/{server_id}", response_model=list[EventRead])
def list_server_events(server_id: int, db: Session = Depends(get_db)):
    return db.query(SecurityEvent).filter(SecurityEvent.server_id == server_id).all()