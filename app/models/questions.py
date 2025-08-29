from abc import ABC, abstractmethod


class Question(ABC):
    def __init__(self, title: str, description: str, reward: int, type: str):
        self.title = title
        self.description = description
        self.reward = reward
        self.type = type

    @property
    @abstractmethod
    def answer(self) -> str | int: ...


class OneAnswer(Question):
    def __init__(self, title: str, description: str, answer: str, reward: int = 1, type: str = "ONE-ANSWER"):
        super().__init__(title=title, description=description, reward=reward, type=type)
        self._answer = answer

    @property
    def answer(self) -> str:
        return self._answer

    @answer.setter
    def answer(self, value: str) -> None:
        self._answer = value


class MultipyChoice(Question):
    def __init__(
        self,
        title: str,
        description: str,
        choices: list,
        answer: int,
        reward: int = 1,
        type: str = "MULTIPLE-CHOICE",
    ):
        super().__init__(title=title, description=description, reward=reward, type=type)
        self._answer = answer
        self.choices = choices

    @property
    def answer(self) -> int:
        return self._answer

    @answer.setter
    def answer(self, value: int) -> None:
        self._answer = value
