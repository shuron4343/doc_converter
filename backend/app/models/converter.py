"""
Pydantic модели для API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class ConversionFormat(str, Enum):
    """Поддерживаемые форматы конвертации"""
    MARKDOWN = "markdown"
    HTML = "html"
    TEXT = "text"


class ConversionOptions(BaseModel):
    """Опции конвертации"""
    preserve_formatting: bool = Field(default=True, description="Сохранять форматирование")
    include_images: bool = Field(default=True, description="Включать изображения")
    max_image_size: int = Field(default=1024, description="Максимальный размер изображения")
    table_format: str = Field(default="grid", description="Формат таблиц")


class ConversionRequest(BaseModel):
    """Запрос на конвертацию"""
    filename: str = Field(..., description="Имя файла")
    options: Optional[ConversionOptions] = Field(default=None, description="Опции конвертации")


class ConversionResponse(BaseModel):
    """Ответ на конвертацию"""
    success: bool = Field(..., description="Успешность конвертации")
    content: Optional[str] = Field(default=None, description="Конвертированный контент")
    filename: Optional[str] = Field(default=None, description="Имя выходного файла")
    error: Optional[str] = Field(default=None, description="Сообщение об ошибке")


class FormatsResponse(BaseModel):
    """Ответ со списком поддерживаемых форматов"""
    formats: List[str] = Field(..., description="Список поддерживаемых форматов")


class HealthResponse(BaseModel):
    """Ответ о состоянии сервера"""
    status: str = Field(..., description="Статус сервера")
    version: str = Field(..., description="Версия приложения")
