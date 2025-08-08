# Document Converter Web App

Веб-приложение для конвертации документов в markdown с помощью docling.

## Возможности

- Конвертация документов различных форматов в markdown
- Поддержка DOCX, PDF и других форматов
- Веб-интерфейс на Vue.js
- REST API на FastAPI
- Загрузка файлов через браузер
- Предварительный просмотр результатов

## Структура проекта

```
doc_converter/
├── backend/                 # FastAPI бэкенд
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI приложение
│   │   ├── api/            # API роуты
│   │   ├── core/           # Конфигурация и настройки
│   │   ├── models/         # Pydantic модели
│   │   ├── services/       # Бизнес-логика
│   │   └── utils/          # Утилиты
│   ├── tests/              # Тесты бэкенда
│   └── requirements.txt    # Зависимости бэкенда
├── frontend/               # Vue.js фронтенд
│   ├── src/
│   │   ├── components/     # Vue компоненты
│   │   ├── views/          # Страницы
│   │   ├── router/         # Маршрутизация
│   │   ├── store/          # Vuex store
│   │   └── assets/         # Статические файлы
│   ├── public/             # Публичные файлы
│   └── package.json        # Зависимости фронтенда
├── shared/                 # Общий код
│   └── converter.py        # Логика конвертации
└── docker-compose.yml      # Docker конфигурация
```

## Установка и запуск

### Backend (FastAPI)

1. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # или
   .venv\Scripts\activate     # Windows
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сервер разработки:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend (Vue.js)

1. Установите Node.js и npm

2. Установите зависимости:
   ```bash
   cd frontend
   npm install
   ```

3. Запустите сервер разработки:
   ```bash
   npm run serve
   ```

### Docker

Запустите всё приложение с помощью Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

- `POST /api/convert` - Конвертация документа
- `GET /api/formats` - Получение поддерживаемых форматов
- `GET /api/health` - Проверка состояния сервера

## Использование

1. Откройте браузер и перейдите на `http://localhost:8080`
2. Загрузите документ через веб-интерфейс
3. Выберите настройки конвертации
4. Нажмите "Конвертировать"
5. Скачайте результат в формате markdown
