from app.adapter import InMemoryDatabase
from app.dto import LeaderboardType
from typing import Any
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from io import BytesIO

from app.deps import get_storage

Storage = get_storage()


class LeaderboardGenerator:

    @staticmethod
    def create_table_leaderboard() -> Any:
        all_users = Storage.get_all_users()
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
        all_users = Storage.get_all_users()

        users_names = [
            user.first_name + " " + user.last_name + "\n id:" + str(user.id)
            for user in all_users
        ]
        users_scores = [user.score for user in all_users]
        buf = BytesIO()
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.xticks(rotation=45)
        if all_users:
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
        if leaderboard_type == LeaderboardType.TABLE:
            return cls.create_table_leaderboard()
        else:
            return cls.create_graph_leaderboard()