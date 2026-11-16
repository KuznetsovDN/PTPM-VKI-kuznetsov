class Controller:
    def __init__(self, user_io, db, notifier, calculator):
        self.user_io = user_io
        self.db = db
        self.notifier = notifier
        self.calculator = calculator

    def run(self):
        # Шаг 1: получить данные
        s1, s2, s3 = self.user_io.get_input()

        # Нормализуем ключ для БД (строки -> float).
        try:
            ka, kb, kc = float(s1), float(s2), float(s3)
        except (TypeError, ValueError):
            ka = kb = kc = None  # для нечисловых в БД не кладём

        # Шаг 2: проверить кэш или посчитать
        cached = self.db.get(ka, kb, kc) if ka is not None else None

        if cached is not None:
            ttype, err = cached
            source = "БД"
        else:
            ttype, err = self.calculator.calculate(s1, s2, s3)
            if ka is not None:
                self.db.add(ka, kb, kc, ttype, err)
            source = "вычисления"

        # Шаг 3: сформировать и отправить строку-результат
        if err:
            result = f"Ошибка: {err}"
        else:
            result = f"Тип треугольника: {ttype}"
        self.notifier.send(result)

        # Шаг 4: вернуть результат
        return {"result": result, "source": source}