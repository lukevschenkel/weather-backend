from abc import ABC, abstractmethod

class BaseMessageProvider(ABC):
    @abstractmethod
    def generate_message(self, data: dict) -> str:
        pass