from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.auth import router as auth_router
from app.api.books import router as book_router
from app.api.borrow import router as borrow_router
from app.api.rfid import router as rfid_router
from app.api.hardware import router as hardware_router

from app.routes.dashboard_routes import router as dashboard_router
from app.routes.page_routes import router as page_router


app = FastAPI(title="Smartlib Ecosystem")

app.add_middleware(
    SessionMiddleware,
    secret_key="SMARTLIB_SESSION_SECRET"
)

@app.get('/')
def home():
    return {'message': 'Smartlib running'}

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(book_router, prefix="/api", tags=["Books"])
app.include_router(borrow_router, prefix="/api", tags=["Borrowing"])
app.include_router(rfid_router, prefix="/api", tags=["RFID"])
app.include_router(hardware_router, prefix="/api/v1/hardware", tags=["Hardware"])

app.include_router(dashboard_router)
app.include_router(page_router)