"""
API роуты для FastAPI
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from app.models.converter import (
    ConversionResponse, 
    FormatsResponse, 
    HealthResponse,
    ConversionOptions
)
from app.services.converter_service import converter_service
from app.core.config import settings

# Создаем роутер
api_router = APIRouter()
logger = logging.getLogger(__name__)


@api_router.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка состояния сервера"""
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )


@api_router.get("/formats", response_model=FormatsResponse)
async def get_supported_formats():
    """Получение списка поддерживаемых форматов"""
    try:
        formats = converter_service.get_supported_formats()
        return FormatsResponse(formats=formats)
    except Exception as e:
        logger.error(f"Ошибка при получении форматов: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")


@api_router.post("/convert", response_model=ConversionResponse)
async def convert_document(
    file: UploadFile = File(...),
    preserve_formatting: bool = Form(default=True),
    include_images: bool = Form(default=True),
    max_image_size: int = Form(default=1024),
    table_format: str = Form(default="grid")
):
    """Конвертация документа в markdown"""
    try:
        # Проверяем размер файла
        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"Файл слишком большой. Максимальный размер: {settings.MAX_FILE_SIZE} байт"
            )
        
        # Проверяем расширение файла
        file_ext = file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        if f'.{file_ext}' not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Неподдерживаемый формат файла. Поддерживаемые форматы: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Читаем содержимое файла
        file_content = await file.read()
        
        # Сохраняем файл временно
        saved_file_path = converter_service.save_uploaded_file(file_content, file.filename)
        
        if not saved_file_path:
            raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")
        
        try:
            # Опции конвертации
            options = {
                "preserve_formatting": preserve_formatting,
                "include_images": include_images,
                "max_image_size": max_image_size,
                "table_format": table_format
            }
            
            # Конвертируем файл
            markdown_content = converter_service.convert_file(saved_file_path, options)
            
            if markdown_content:
                # Генерируем имя выходного файла
                output_filename = f"{file.filename.rsplit('.', 1)[0]}.md"
                
                return ConversionResponse(
                    success=True,
                    content=markdown_content,
                    filename=output_filename
                )
            else:
                return ConversionResponse(
                    success=False,
                    error="Не удалось конвертировать файл"
                )
                
        finally:
            # Удаляем временный файл
            converter_service.cleanup_file(saved_file_path)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при конвертации: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@api_router.get("/")
async def api_root():
    """Корневой endpoint API"""
    return {
        "message": "Document Converter API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "formats": "/formats",
            "convert": "/convert"
        }
    }
