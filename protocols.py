from typing import Protocol, Any

class Processable(Protocol):
    def __call__(self, data: Any) -> Any:
        ...