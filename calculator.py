from triangle import process_triangle


class TriangleCalculator:
    """
    Класс вычислений (пункт a).
    Оборачивает логику ЛР1 в один метод calculate().
    Возвращает (тип_треугольника, сообщение_об_ошибке).
    Второй элемент None, если ошибки нет.
    """

    def calculate(self, s1: str, s2: str, s3: str):
        ttype, vertices = process_triangle(s1, s2, s3)

        # Сигнатура ошибки валидации из process_triangle — (-2, -2)
        if vertices == [(-2, -2), (-2, -2), (-2, -2)]:
            return None, f"Некорректные входные данные: {s1!r}, {s2!r}, {s3!r}"

        # Сигнатура «не треугольник»
        if ttype == "не треугольник":
            return None, "Стороны не образуют треугольник"

        return ttype, None