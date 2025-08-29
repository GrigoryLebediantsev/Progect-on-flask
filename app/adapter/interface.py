from typing import Protocol
from app.models.expressions import Expression
from app.models.users import User


class DatabaseInterface(Protocol):
    def create_expression(self, expression: Expression) -> int: ...
    def get_expression(self, expression_id: int) -> Expression: ...

    def get_user(self, user_id: int) -> User: ...

    # Сюда добавлять функции которые будут использоваться в приложении, от интерфейса
