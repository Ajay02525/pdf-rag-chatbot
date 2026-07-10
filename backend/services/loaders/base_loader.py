from abc import ABC, abstractmethod


class BaseLoader(ABC):
    @staticmethod
    @abstractmethod
    def load(path):
        pass
