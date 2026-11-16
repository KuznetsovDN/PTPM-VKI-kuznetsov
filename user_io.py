from abc import ABC, abstractmethod


class UserIO(ABC):
    """Интерфейс взаимодействия с пользователем."""

    @abstractmethod
    def get_input(self):
        """Возвращает кортеж строк (s1, s2, s3)."""
        pass


class ConsoleUserIO(UserIO):
    """Реализация через input()."""

    def get_input(self):
        s1 = input("Сторона A: ")
        s2 = input("Сторона B: ")
        s3 = input("Сторона C: ")
        return s1, s2, s3