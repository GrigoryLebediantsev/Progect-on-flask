FROM python:3.12


# Делаем рабочую папку внутри контейнера
WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN pip install --upgrade pip
RUN pip install uv

# Устанавливаем зависимости и сам проект (по lock-файлу, если он есть)
RUN uv sync --no-dev

# Добавляем виртуальное окружение в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Копируем все файлы проекта в контейнер
COPY . /app/

# Запускаем Flask-приложение
CMD ["python", "-m", "app.main"]