from abc import *

class ActivityBase():
    @abstractmethod
    def get_answer(self, idx: int) -> str:
        pass

    @abstractmethod
    def get_all_words(self) -> str:
        pass