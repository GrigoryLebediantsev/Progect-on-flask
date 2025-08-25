from abc import ABC, abstractmethod


class Question(ABC):
    def __init__(self, id: int, title: str, description: str, reward=None):
        self.id = id
        self.description = description
        self.title = title
        if reward is None:
            reward = 1
        self.reward = reward

    @property
    @abstractmethod
    def answer(self):
        pass


class OneAnswer(Question):
    def __init__(self, id: int, title: str, description: str, answer: str, reward=None):
        super().__init__(id, title, description, reward)
        self._answer = answer

    @property
    def answer(self) -> str:
        return self._answer

    @answer.setter
    def answer(self, value: str):
        self._answer = value

    @staticmethod
    def is_valid(answer) -> bool:
        return isinstance(answer, str)

    def __repr__(self) -> str:
        return f"{self.id}) {self.title}"

    def to_dict(self):
        return dict(
            {
                "title": self.title,
                "description": self.description,
                "type": "ONE-ANSWER",
                "answer": self.answer,
            }
        )


class MultipyChoice(Question):
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        choices: list,
        answer: int,
        reward=None,
    ):
        super().__init__(id, title, description, reward)
        self._answer = answer
        self.choices = choices

    @property
    def answer(self) -> int:
        return self._answer

    @answer.setter
    def answer(self, value: int):
        self._answer = value

    @staticmethod
    def is_valid(answer, choices) -> bool:
        if not isinstance(answer, int) or answer < 0 or answer > len(choices):
            return False
        return True

    def __repr__(self):
        return f"{self.id}) {self.title}"

    def to_dict(self):
        return dict(
            {
                "title": self.title,
                "description": self.description,
                "type": "ONE-ANSWER",
                "choices": self.choices,
                "reward": self.reward,
                "answer": self.answer,
            }
        )
