from app.adapter.in_memory import InMemoryDatabase

_HISTORY_ALL_USERS: dict[int, dict] = {}


class UserHistory:
    @staticmethod
    def create_user_history(user_id: int) -> None:
        _HISTORY_ALL_USERS[user_id] = {"history": []}

    @staticmethod
    def get_user_history(user_id: int) -> dict:
        return _HISTORY_ALL_USERS[user_id]

    @staticmethod
    def add_to_user_history(user_id: int, data_to_history: dict) -> None:
        _HISTORY_ALL_USERS[user_id]["history"].append(data_to_history)
