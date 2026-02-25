from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import init_db, SessionLocal
from models import Server, SecurityPolicy, SecurityEvent

app = FastAPI(title="Администрирование ИБ — MVP")
init_db()

templates = Jinja2Templates(directory="templates")

# зависимость для сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== Dashboard =====
@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    servers_count = db.query(Server).count()
    policies_count = db.query(SecurityPolicy).count()
    events_count = db.query(SecurityEvent).count()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "servers_count": servers_count,
        "policies_count": policies_count,
        "events_count": events_count
    })

# ===== Servers Page =====
@app.get("/servers")
def servers_list(request: Request, db: Session = Depends(get_db)):
    servers = db.query(Server).all()
    return templates.TemplateResponse("servers.html", {"request": request, "servers": servers})

@app.get("/servers/create")
def server_create_form(request: Request):
    return templates.TemplateResponse("server_form.html", {"request": request, "action": "create"})

@app.post("/servers/create")
def server_create(request: Request, name: str = Form(...), ip_address: str = Form(...), status: str = Form("online"), db: Session = Depends(get_db)):
    server = Server(name=name, ip_address=ip_address, status=status)
    db.add(server)
    db.commit()
    return templates.TemplateResponse("servers.html", {"request": request, "servers": db.query(Server).all()})

@app.get("/servers/edit/{server_id}")
def server_edit_form(request: Request, server_id: int, db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == server_id).first()
    return templates.TemplateResponse("server_form.html", {"request": request, "server": server, "action": "edit"})

@app.post("/servers/edit/{server_id}")
def server_edit(request: Request, server_id: int, name: str = Form(...), ip_address: str = Form(...), status: str = Form("online"), db: Session = Depends(get_db)):
    server = db.query(Server).filter(Server.id == server_id).first()
    server.name = name
    server.ip_address = ip_address
    server.status = status
    db.commit()
    return templates.TemplateResponse("servers.html", {"request": request, "servers": db.query(Server).all()})

@app.post("/servers/delete/{server_id}")
def server_delete(server_id: int, db: Session = Depends(get_db), request: Request = None):
    server = db.query(Server).filter(Server.id == server_id).first()
    db.delete(server)
    db.commit()
    servers = db.query(Server).all()
    return templates.TemplateResponse("servers.html", {"request": request, "servers": servers})

# ===== Policies =====
@app.get("/policies")
def policies_list(request: Request, db: Session = Depends(get_db)):
    policies = db.query(SecurityPolicy).all()
    return templates.TemplateResponse("policies.html", {"request": request, "policies": policies})

@app.get("/policies/create")
def policy_create_form(request: Request):
    return templates.TemplateResponse("policy_form.html", {"request": request, "action": "create"})

@app.post("/policies/create")
def policy_create(request: Request, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    policy = SecurityPolicy(name=name, description=description)
    db.add(policy)
    db.commit()
    return templates.TemplateResponse("policies.html", {"request": request, "policies": db.query(SecurityPolicy).all()})

@app.get("/policies/edit/{policy_id}")
def policy_edit_form(request: Request, policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(SecurityPolicy).filter(SecurityPolicy.id==policy_id).first()
    return templates.TemplateResponse("policy_form.html", {"request": request, "policy": policy, "action": "edit"})

@app.post("/policies/edit/{policy_id}")
def policy_edit(request: Request, policy_id: int, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    policy = db.query(SecurityPolicy).filter(SecurityPolicy.id==policy_id).first()
    policy.name = name
    policy.description = description
    db.commit()
    return templates.TemplateResponse("policies.html", {"request": request, "policies": db.query(SecurityPolicy).all()})

@app.post("/policies/delete/{policy_id}")
def policy_delete(request: Request, policy_id: int, db: Session = Depends(get_db)):
    policy = db.query(SecurityPolicy).filter(SecurityPolicy.id==policy_id).first()
    db.delete(policy)
    db.commit()
    return templates.TemplateResponse("policies.html", {"request": request, "policies": db.query(SecurityPolicy).all()})

# ===== Events =====
@app.get("/events")
def events_list(request: Request, db: Session = Depends(get_db)):
    events = db.query(SecurityEvent).all()
    servers = db.query(Server).all()
    policies = db.query(SecurityPolicy).all()
    return templates.TemplateResponse("events.html", {"request": request, "events": events, "servers": servers, "policies": policies})

@app.get("/events/create")
def event_create_form(request: Request, db: Session = Depends(get_db)):
    servers = db.query(Server).all()
    policies = db.query(SecurityPolicy).all()
    return templates.TemplateResponse("event_form.html", {"request": request, "servers": servers, "policies": policies, "action": "create"})

@app.post("/events/create")
def event_create(request: Request, server_id: int = Form(...), policy_id: int = Form(...),
                 event_type: str = Form(...), severity: str = Form(...), description: str = Form(""),
                 db: Session = Depends(get_db)):
    event = SecurityEvent(server_id=server_id, policy_id=policy_id, event_type=event_type,
                          severity=severity, description=description)
    db.add(event)
    db.commit()
    events = db.query(SecurityEvent).all()
    servers = db.query(Server).all()
    policies = db.query(SecurityPolicy).all()
    return templates.TemplateResponse("events.html", {"request": request, "events": events, "servers": servers, "policies": policies})

@app.get("/events/edit/{event_id}")
def event_edit_form(request: Request, event_id: int, db: Session = Depends(get_db)):
    event = db.query(SecurityEvent).filter(SecurityEvent.id==event_id).first()
    servers = db.query(Server).all()
    policies = db.query(SecurityPolicy).all()
    return templates.TemplateResponse("event_form.html", {"request": request, "event": event, "servers": servers, "policies": policies, "action": "edit"})

@app.post("/events/edit/{event_id}")
def event_edit(request: Request, event_id: int, server_id: int = Form(...), policy_id: int = Form(...),
               event_type: str = Form(...), severity: str = Form(...), description: str = Form(""),
               db: Session = Depends(get_db)):
    event = db.query(SecurityEvent).filter(SecurityEvent.id==event_id).first()
    event.server_id = server_id
    event.policy_id = policy_id
    event.event_type = event_type
    event.severity = severity
    event.description = description
    db.commit()
    events = db.query(SecurityEvent).all()
    servers = db.query(Server).all()
    policies = db.query(SecurityPolicy).all()
    return templates.TemplateResponse("events.html", {"request": request, "events": events, "servers": servers, "policies": policies})

@app.post("/events/delete/{event_id}")
def event_delete(request: Request, event_id: int, db: Session = Depends(get_db)):
    event = db.query(SecurityEvent).filter(SecurityEvent.id==event_id).first()
    db.delete(event)
    db.commit()
    events = db.query(SecurityEvent).all()
    servers = db.query(Server).all()
    policies = db.query(SecurityPolicy).all()
    return templates.TemplateResponse("events.html", {"request": request, "events": events, "servers": servers, "policies": policies})