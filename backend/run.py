#!/usr/bin/env python3
"""
Скрипт для запуска FastAPI приложения
"""

import uvicorn
import sys
import os

# Добавляем путь к shared модулю
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
