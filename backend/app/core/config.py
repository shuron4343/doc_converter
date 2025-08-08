"""
Конфигурация приложения
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    APP_NAME: str = "Document Converter"
    DEBUG: bool = False
    VERSION: str = "0.1.0"
    
    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS настройки
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Настройки загрузки файлов
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".docx", ".pdf", ".txt", ".rtf"]
    
    # Настройки конвертации
    OUTPUT_DIR: str = "output"
    PRESERVE_FORMATTING: bool = True
    INCLUDE_IMAGES: bool = True
    MAX_IMAGE_SIZE: int = 1024
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создаем экземпляр настроек
settings = Settings()
