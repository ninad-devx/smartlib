from app.models.audit import AuditLog

def log_action(db, action: str, user_id: int):
    log = AuditLog(
        action=action,
        performed_by=user_id
    )

    db.add(log)
    db.commit()