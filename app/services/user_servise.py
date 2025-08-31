from typing import Any
import matplotlib
matplotlib.use("Agg")
from app.dto.users import GenerateUserInput
from app.adapter.in_memory import InMemoryDatabase
from app.adapter.history import UserHistory
from app.models.users import User
from matplotlib import pyplot as plt
from io import BytesIO


class UserService:

    @staticmethod
    def create_user(user_input: GenerateUserInput) -> User:

        user = User(**user_input.model_dump())
        InMemoryDatabase.add_user(user)
        UserHistory.create_user_history(user.id)

        return user

    @staticmethod
    def create_table_leaderboard() -> Any:
        all_users = InMemoryDatabase.get_all_users()
        all_users_sort = sorted(all_users, key=lambda u: u.score, reverse=True)
        return [
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "score": user.score,
            }
            for user in all_users_sort
        ]

    @staticmethod
    def create_graph_leaderboard():
        all_users = InMemoryDatabase.get_all_users()



        users_names = [
            user.first_name + " " + user.last_name + "\n id:" + str(user.id)
            for user in all_users
        ]
        users_scores = [user.score for user in all_users]
        buf = BytesIO()
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.xticks(rotation=45)
        if all_users:
            # ax.set_xlim()
            ax.set_ylim(bottom=0, top=(max(users_scores) + 1))
        ax.bar(x=users_names, height=users_scores)
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        data = buf.getvalue()
        return data

    @classmethod
    def create_leaderboard(cls, leaderboard_type: str) -> Any:
        if leaderboard_type == "table":
            return cls.create_table_leaderboard()
        elif leaderboard_type == "graph":
            return cls.create_graph_leaderboard()
        else:
            raise ValueError("Не корректная информация типа данных")
