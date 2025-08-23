import random


class Expression:
    OPERATIONS = ["+", "*", "-", "//", "**"]
    def __init__(self, id, operation, *values, reward=None):

        if reward is None:
            reward = len(values) - 1

        if not (
            isinstance(id, int)
            and isinstance(operation, str)
            and isinstance(values, tuple)
            and isinstance(reward, int)
        ):
            raise ValueError

        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()
        self.reward = reward

    def __evaluate(self):
        return eval(self.to_str)

    @property
    def to_str(self):
        str_values = list(map(str, self.values))
        expr_str = f" {self.operation} ".join(str_values)
        return expr_str

    def __repr__(self):
        return f"{self.id}) {self.to_str} = {self.answer}"

    @staticmethod
    def choose_operation(operation: str) -> str:
        """Возвращает конкретную операцию для Expression"""
        if operation == "random":
            operation = random.choice(["+", "*", "-", "//", "**"])
        if operation not in Expression.OPERATIONS:
            raise ValueError(f"Недопустимая операция: {operation}")
        return operation

    @staticmethod
    def validate_expression_params(count_nums: int, operation: str) -> bool:
        """
        Проверяет, допустимо ли количество чисел для данной операции.
        Для операций +, *, ** можно больше 2 чисел.
        Для остальных только 2 числа.
        """
        if count_nums <= 1:
            return False
        if count_nums > 2 and operation not in {"+", "*", "**"}:
            return False
        return True

    def check_answer(self, user_answer, user):
        """
        Проверяет ответ пользователя и увеличивает его score при верном ответе.
        Возвращает "correct" или "wrong".
        """
        if user_answer == self.answer:
            user.increase_score(self.reward)
            return "correct"
        return "wrong"