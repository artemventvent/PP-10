from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Server
from schemas import ServerCreate, ServerRead

router = APIRouter()

# зависимость для сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ServerRead)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    db_server = Server(name=server.name, ip_address=server.ip_address)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

@router.get("/", response_model=list[ServerRead])
def list_servers(db: Session = Depends(get_db)):
    return db.query(Server).all()