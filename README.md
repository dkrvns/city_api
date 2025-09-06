## Установка
# Виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate
poetry install
```

# docker-compose
```
docker compose up -d
```

# Миграции
```
alembic upgrade head
```

# Запуск сервера
После всех манипуляций надо найти main.py в самом корне(их два, внимательнее) и просто запустить его. Сваггер будет доступен по адресу `127.0.0.1:8000/docs`
