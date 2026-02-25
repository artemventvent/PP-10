from pydantic import BaseModel
from typing import Optional
import datetime

class ServerBase(BaseModel):
    name: str
    ip_address: str

class ServerCreate(ServerBase):
    pass

class ServerRead(ServerBase):
    id: int
    status: str

    class Config:
        orm_mode = True

class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None

class PolicyCreate(PolicyBase):
    pass

class PolicyRead(PolicyBase):
    id: int

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    server_id: int
    policy_id: int
    event_type: str
    severity: str = "low"
    description: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True