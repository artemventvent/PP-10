from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    status = Column(String, default="online")  # online/offline/warning
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    services = relationship("Service", back_populates="server")
    events = relationship("SecurityEvent", back_populates="server")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("servers.id"))
    name = Column(String, nullable=False)
    status = Column(String, default="running")  # running/stopped
    server = relationship("Server", back_populates="services")

class SecurityPolicy(Base):
    __tablename__ = "security_policies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    events = relationship("SecurityEvent", back_populates="policy")

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("servers.id"))
    policy_id = Column(Integer, ForeignKey("security_policies.id"))
    event_type = Column(String, nullable=False)
    severity = Column(String, default="low")  # low/medium/high
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    server = relationship("Server", back_populates="events")
    policy = relationship("SecurityPolicy", back_populates="events")