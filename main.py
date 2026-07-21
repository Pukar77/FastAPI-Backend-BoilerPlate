import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.api.auth import router as auth_router
from app.api.product import router as product_router
from app.api.cart import router as cart_router
from app.api.order import router as order_router
from app.core.exceptions import AppException
from app.core.config import get_settings

app = FastAPI()

settings = get_settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)





