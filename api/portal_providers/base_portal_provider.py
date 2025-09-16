from abc import ABC, abstractmethod
from typing import TypedDict

class MessagePayload(TypedDict):
    message: str


class BasePortalProvider(ABC):

    @abstractmethod
    def push_message(self, data: MessagePayload) -> dict:
        pass