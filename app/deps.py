from app.adapter.database import Database
from app.adapter.memory import InMemoryDatabase

# Тут можно поменять реализацию «одним кликом»
STORAGE_TYPE = "db"  # или "db"

def get_storage():
    if STORAGE_TYPE == "memory":
        return InMemoryDatabase()
    elif STORAGE_TYPE == "db":
        return Database() # передай своё соединение с БД
    else:
        raise ValueError("Unknown storage type")
