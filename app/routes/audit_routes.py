from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.core.database import Sessionlocal
from app.models.audit import AuditLog

from app.utils.auth import (
    require_login,
    require_role
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@router.get("/audit-logs")
def audit_logs_page(
    request: Request
):

    require_login(request)

    require_role(
        request,
        ["librarian"]
    )

    db = Sessionlocal()

    logs = (
        db.query(AuditLog)
        .order_by(
            AuditLog.id.desc()
        )
        .limit(300)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="audit_logs.html",
        context={
            "request": request,
            "logs": logs
        }
    )