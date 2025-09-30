FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Делаем рабочую папку внутри контейнера
WORKDIR /app

COPY pyproject.toml uv.lock /app/

# Устанавливаем зависимости и сам проект (по lock-файлу, если он есть)
RUN uv sync --no-dev

# Добавляем виртуальное окружение в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Копируем все файлы проекта в контейнер
COPY . /app/

# Запускаем Flask-приложение
CMD ["python", "main.py"]