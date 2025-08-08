"""
Сервис для конвертации документов
"""

import os
import tempfile
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import sys

# Добавляем путь к shared модулю
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared'))

from converter import DocumentConverter
from app.core.config import settings


class ConverterService:
    """Сервис для конвертации документов"""
    
    def __init__(self):
        """Инициализация сервиса"""
        self.converter = DocumentConverter()
        self.logger = logging.getLogger(__name__)
        
        # Создаем директории если их нет
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    
    def convert_file(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Конвертирует файл в markdown
        
        Args:
            file_path: Путь к файлу
            options: Опции конвертации
            
        Returns:
            Markdown контент или None при ошибке
        """
        try:
            # Проверяем поддерживается ли формат
            if not self.converter.is_supported_format(file_path):
                self.logger.error(f"Неподдерживаемый формат файла: {file_path}")
                return None
            
            # Конвертируем файл
            markdown_content = self.converter.convert_to_string(file_path)
            
            if markdown_content:
                self.logger.info(f"Файл успешно конвертирован: {file_path}")
                return markdown_content
            else:
                self.logger.error(f"Не удалось конвертировать файл: {file_path}")
                return None
                
        except Exception as e:
            self.logger.error(f"Ошибка при конвертации файла {file_path}: {e}")
            return None
    
    def get_supported_formats(self) -> list:
        """
        Возвращает список поддерживаемых форматов
        
        Returns:
            Список поддерживаемых форматов
        """
        return self.converter.get_supported_formats()
    
    def validate_file(self, file_path: str) -> bool:
        """
        Проверяет валидность файла
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            True если файл валиден
        """
        try:
            file = Path(file_path)
            
            # Проверяем существование файла
            if not file.exists():
                return False
            
            # Проверяем размер файла
            if file.stat().st_size > settings.MAX_FILE_SIZE:
                return False
            
            # Проверяем расширение файла
            if file.suffix.lower() not in settings.ALLOWED_EXTENSIONS:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при валидации файла {file_path}: {e}")
            return False
    
    def save_uploaded_file(self, file_content: bytes, filename: str) -> Optional[str]:
        """
        Сохраняет загруженный файл
        
        Args:
            file_content: Содержимое файла
            filename: Имя файла
            
        Returns:
            Путь к сохраненному файлу или None при ошибке
        """
        try:
            file_path = os.path.join(settings.UPLOAD_DIR, filename)
            
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            self.logger.info(f"Файл сохранен: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении файла {filename}: {e}")
            return None
    
    def cleanup_file(self, file_path: str) -> None:
        """
        Удаляет временный файл
        
        Args:
            file_path: Путь к файлу
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.logger.info(f"Файл удален: {file_path}")
        except Exception as e:
            self.logger.error(f"Ошибка при удалении файла {file_path}: {e}")


# Создаем экземпляр сервиса
converter_service = ConverterService()
