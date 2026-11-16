import logging
import sys
import os

from triangle import process_triangle


def setup_logging() -> None:
    """Настройка сквозного логирования: консоль + файл."""
    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Создаём папку для логов, если её нет
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
        ],
    )


def main() -> None:
    setup_logging()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    # Пример входных данных (строки, как требует задание)
    tests = [
        ("3", "3", "3"),          # равносторонний
        ("5", "5", "8"),          # равнобедренный
        ("3", "4", "5"),          # разносторонний
        ("1", "2", "10"),         # не треугольник
        ("abc", "4", "5"),        # нечисловые данные
        ("-3", "4", "5"),         # отрицательное значение
        ("0", "4", "5"),          # нулевая сторона
        ("3.5", "4.5", "5.5"),    # вещественные
    ]

    for s1, s2, s3 in tests:
        logging.info(f"Запрос: A={s1!r}, B={s2!r}, C={s3!r}")
        try:
            triangle_type, vertices = process_triangle(s1, s2, s3)
            logging.info(
                f"Результат: тип={triangle_type!r}, вершины={vertices}"
            )
        except Exception:
            logging.exception(
                f"Неуспешный запрос: A={s1!r}, B={s2!r}, C={s3!r}"
            )

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()