from typing import Optional


class Expression:

    def __init__(self, operation: str, values: list[int], reward: int):

        self.operation = operation
        self.values = values
        self.answer = self._evaluate()
        self.reward = reward
        self.id: Optional[int] = None

    def _evaluate(self) -> int:
        return eval(self._to_str)

    @property
    def _to_str(self) -> str:
        str_values = list(map(str, self.values))
        expr_str = f" {self.operation} ".join(str_values)
        return expr_str

    def check_answer(self, user_answer: int) -> bool:
        if user_answer == self.answer:
            return True
        return False
