#!/usr/bin/env python3
import datetime
from database import SessionLocal, init_db
from models import Server, SecurityPolicy, SecurityEvent, Service, Role, User

def seed_database():
    init_db()
    session = SessionLocal()
    
    # Clear existing data
    session.query(SecurityEvent).delete()
    session.query(SecurityPolicy).delete()
    session.query(Service).delete()
    session.query(Server).delete()
    session.query(User).delete()
    session.query(Role).delete()
    session.commit()
    
    # Create roles
    admin_role = Role(name="admin")
    user_role = Role(name="user")
    session.add_all([admin_role, user_role])
    session.commit()
    
    # Create servers
    servers = [
        Server(name="Web-Server-01", ip_address="192.168.1.10", status="online"),
        Server(name="DB-Server-01", ip_address="192.168.1.20", status="online"),
        Server(name="API-Server-01", ip_address="192.168.1.30", status="online"),
        Server(name="Cache-Server-01", ip_address="192.168.1.40", status="warning"),
        Server(name="Mail-Server-01", ip_address="192.168.1.50", status="offline"),
    ]
    session.add_all(servers)
    session.commit()
    
    # Create services for servers
    services = [
        Service(server_id=1, name="Apache", status="running"),
        Service(server_id=1, name="OpenSSH", status="running"),
        Service(server_id=2, name="PostgreSQL", status="running"),
        Service(server_id=2, name="pgBackRest", status="running"),
        Service(server_id=3, name="Node.js", status="running"),
        Service(server_id=3, name="PM2", status="running"),
        Service(server_id=4, name="Redis", status="running"),
        Service(server_id=5, name="Postfix", status="stopped"),
        Service(server_id=5, name="Dovecot", status="stopped"),
    ]
    session.add_all(services)
    session.commit()
    
    # Create security policies
    policies = [
        SecurityPolicy(name="Firewall Rules", description="Основные правила фаерволла для сегментации сети"),
        SecurityPolicy(name="Access Control", description="Политика контроля доступа и управления правами"),
        SecurityPolicy(name="Encryption", description="Требования к шифрованию данных в покое и в пути"),
        SecurityPolicy(name="Patch Management", description="Процесс управления и обновлением уязвимостей"),
        SecurityPolicy(name="Logging & Monitoring", description="Политика логирования и мониторинга системы"),
    ]
    session.add_all(policies)
    session.commit()
    
    # Create security events
    base_time = datetime.datetime.utcnow()
    events = [
        SecurityEvent(
            server_id=1, policy_id=1, event_type="access_denied",
            severity="high", description="Попытка несанкционированного доступа с IP 203.0.113.5",
            timestamp=base_time - datetime.timedelta(hours=2)
        ),
        SecurityEvent(
            server_id=2, policy_id=4, event_type="patch_required",
            severity="medium", description="PostgreSQL требует критического обновления безопасности",
            timestamp=base_time - datetime.timedelta(hours=1)
        ),
        SecurityEvent(
            server_id=1, policy_id=5, event_type="audit_log",
            severity="low", description="Успешное логирование администратора",
            timestamp=base_time - datetime.timedelta(minutes=30)
        ),
        SecurityEvent(
            server_id=3, policy_id=2, event_type="permission_change",
            severity="medium", description="Изменение прав доступа на файл конфигурации",
            timestamp=base_time - datetime.timedelta(minutes=15)
        ),
        SecurityEvent(
            server_id=4, policy_id=5, event_type="performance_warning",
            severity="medium", description="Redis использует 85% памяти",
            timestamp=base_time - datetime.timedelta(minutes=5)
        ),
        SecurityEvent(
            server_id=5, policy_id=1, event_type="service_down",
            severity="high", description="Mail сервис недоступен, firewall правило заблокировало порт 25",
            timestamp=base_time - datetime.timedelta(hours=3)
        ),
        SecurityEvent(
            server_id=2, policy_id=3, event_type="ssl_certificate",
            severity="high", description="SSL сертификат истекает через 30 дней",
            timestamp=base_time - datetime.timedelta(days=1)
        ),
    ]
    session.add_all(events)
    session.commit()
    
    print("БД заполнена тестовыми данными")
    print(f"  - Серверов: {session.query(Server).count()}")
    print(f"  - Сервисов: {session.query(Service).count()}")
    print(f"  - Политик: {session.query(SecurityPolicy).count()}")
    print(f"  - События: {session.query(SecurityEvent).count()}")
    
    session.close()

if __name__ == "__main__":
    seed_database()
