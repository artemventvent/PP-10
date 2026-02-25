from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SecurityPolicy
from schemas import PolicyCreate, PolicyRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PolicyRead)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    db_policy = SecurityPolicy(name=policy.name, description=policy.description)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.get("/", response_model=list[PolicyRead])
def list_policies(db: Session = Depends(get_db)):
    return db.query(SecurityPolicy).all()