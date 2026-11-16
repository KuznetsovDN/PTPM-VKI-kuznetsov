import logging
import math

# Размер поля отрисовки
FIELD_SIZE = 100
MARGIN = 10  # отступ от краёв, чтобы треугольник помещался целиком


def _parse_side(value: str) -> float:
    """
    Преобразует строку в положительное вещественное число.
    Бросает ValueError при некорректных данных.
    """
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Нечисловое значение: {value!r}")

    if number <= 0 or math.isnan(number) or math.isinf(number):
        raise ValueError(f"Сторона должна быть положительным числом: {value!r}")

    return number


def _is_triangle(a: float, b: float, c: float) -> bool:
    """Проверка неравенства треугольника (строгое)."""
    return a + b > c and a + c > b and b + c > a


def _triangle_type(a: float, b: float, c: float) -> str:
    """Определяет вид треугольника по трём сторонам."""
    if not _is_triangle(a, b, c):
        return "не треугольник"

    if math.isclose(a, b) and math.isclose(b, c):
        return "равносторонний"
    if math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
        return "равнобедренный"
    return "разносторонний"


def _compute_vertices(a: float, b: float, c: float):
    """
    Вычисляет координаты трёх вершин треугольника,
    вписанного в поле FIELD_SIZE x FIELD_SIZE.

    Возвращает список кортежей (int, int).
    """
    # Помещаем сторону A горизонтально: вершина A в начале координат,
    # вершина B — на оси X.
    ax, ay = 0.0, 0.0
    bx, by = a, 0.0

    # Координаты третьей вершины через теорему косинусов
    cos_angle = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
    # Ограничиваем косинус для устойчивости вычислений
    cos_angle = max(-1.0, min(1.0, cos_angle))
    angle = math.acos(cos_angle)

    cx = c * math.cos(angle)
    cy = c * math.sin(angle)

    # Масштабируем треугольник под поле
    max_x = max(ax, bx, cx)
    max_y = max(ay, by, cy)
    min_x = min(ax, bx, cx)
    min_y = min(ay, by, cy)

    width = max_x - min_x
    height = max_y - min_y

    available = FIELD_SIZE - 2 * MARGIN
    scale = 1.0
    if width > 0 and height > 0:
        scale = min(available / width, available / height)

    # Сдвигаем так, чтобы минимальные координаты попали в MARGIN
    def transform(x: float, y: float):
        sx = (x - min_x) * scale + MARGIN
        sy = (y - min_y) * scale + MARGIN
        return int(round(sx)), int(round(sy))

    vertices = [transform(ax, ay), transform(bx, by), transform(cx, cy)]
    return vertices


def process_triangle(s1: str, s2: str, s3: str):
    """
    Основной метод варианта 1.

    :param s1: строка с длиной стороны A
    :param s2: строка с длиной стороны B
    :param s3: строка с длиной стороны C
    :return: (тип_треугольника: str, координаты: list[tuple[int, int]])
    """
    logging.debug(f"Входные данные: {s1!r}, {s2!r}, {s3!r}")

    # 1. Проверяем, что все три строки — числа
    try:
        a = _parse_side(s1)
        b = _parse_side(s2)
        c = _parse_side(s3)
    except ValueError as ex:
        # Нечисловые / некорректные данные
        logging.error(f"Ошибка валидации входных данных: {ex}")
        logging.exception("Трассировка:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    logging.debug(f"Разобранные стороны: A={a}, B={b}, C={c}")

    # 2. Проверяем неравенство треугольника
    if not _is_triangle(a, b, c):
        logging.warning("Стороны не образуют треугольник")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # 3. Определяем тип
    t_type = _triangle_type(a, b, c)

    # 4. Вычисляем координаты
    try:
        vertices = _compute_vertices(a, b, c)
    except Exception as ex:
        logging.exception(f"Ошибка при вычислении координат: {ex}")
        return t_type, [(-1, -1), (-1, -1), (-1, -1)]

    logging.debug(f"Тип: {t_type}, координаты: {vertices}")
    return t_type, vertices
