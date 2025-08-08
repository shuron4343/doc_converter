"""
Основное FastAPI приложение
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os

# Добавляем путь к shared модулю
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from app.api.routes import api_router
from app.core.config import settings

app = FastAPI(
    title="Document Converter API",
    description="API для конвертации документов в markdown",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API роуты
app.include_router(api_router, prefix="/api")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Корневой endpoint"""
    return {"message": "Document Converter API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    """Проверка состояния сервера"""
    return {"status": "healthy"}
