from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.attendance import Attendancelog

from app.models.audit import AuditLog

from app.utils.auth import (
    require_login,
    require_role
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@router.get("/audit-logs")
def audit_logs_page(
    request: Request,
    db: Session = Depends(get_db)
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )

    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.id.desc())
        .limit(300)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="audit_Logs.html",
        context={
            "logs": logs
        }
    )


@router.post("/audit/clear")
def clear_audit_logs(
    db:Session=Depends(get_db)
):

    db.query(
        AuditLog
    ).delete()

    db.commit()

    return {
        "success":True
    }

@router.post("/attendance/clear")
def clear_attendance_logs(
    db: Session = Depends(get_db)
):

    db.query(
        Attendancelog
    ).delete()

    db.commit()

    return {"success": True}

