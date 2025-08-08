"""
Утилиты для работы с файлами и конфигурацией
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Загружает конфигурацию из файла
    
    Args:
        config_path: Путь к файлу конфигурации
        
    Returns:
        Словарь с конфигурацией
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        return {}
    
    if config_file.suffix.lower() == '.json':
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif config_file.suffix.lower() in ['.yml', '.yaml']:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(f"Неподдерживаемый формат конфигурации: {config_file.suffix}")


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Сохраняет конфигурацию в файл
    
    Args:
        config: Конфигурация для сохранения
        config_path: Путь к файлу конфигурации
    """
    config_file = Path(config_path)
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    if config_file.suffix.lower() == '.json':
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    elif config_file.suffix.lower() in ['.yml', '.yaml']:
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    else:
        raise ValueError(f"Неподдерживаемый формат конфигурации: {config_file.suffix}")


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Получает информацию о файле
    
    Args:
        file_path: Путь к файлу
        
    Returns:
        Словарь с информацией о файле
    """
    file = Path(file_path)
    
    if not file.exists():
        return {"error": "Файл не найден"}
    
    return {
        "name": file.name,
        "size": file.stat().st_size,
        "extension": file.suffix.lower(),
        "modified": file.stat().st_mtime,
        "is_file": file.is_file(),
        "is_dir": file.is_dir()
    }


def ensure_output_dir(output_path: str) -> None:
    """
    Создает директорию для выходного файла если её нет
    
    Args:
        output_path: Путь к выходному файлу
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)


def validate_input_file(input_path: str) -> bool:
    """
    Проверяет существование входного файла
    
    Args:
        input_path: Путь к входному файлу
        
    Returns:
        True если файл существует и доступен для чтения
    """
    input_file = Path(input_path)
    return input_file.exists() and input_file.is_file()


def get_default_config() -> Dict[str, Any]:
    """
    Возвращает конфигурацию по умолчанию
    
    Returns:
        Словарь с конфигурацией по умолчанию
    """
    return {
        "output_format": "markdown",
        "encoding": "utf-8",
        "preserve_formatting": True,
        "include_images": True,
        "max_image_size": 1024,
        "table_format": "grid"
    }
