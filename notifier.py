from abc import ABC, abstractmethod


class Notifier(ABC):
    """Интерфейс отправки данных на внешний сервис."""

    @abstractmethod
    def send(self, message: str) -> bool:
        pass


class EmailNotifier(Notifier):
    """Имитация отправки на email-сервер."""

    def send(self, message: str) -> bool:
        print(f"[EMAIL-SENT] {message}")
        return True