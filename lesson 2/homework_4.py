"""
Задание №4 (дополнительное)
Описание: Валидатор ИНН (идентификационного номера налогоплательщика).
Программа проверяет корректность 10-значных ИНН (организации)
и 12-значных ИНН (физические лица и ИП) с помощью математических алгоритмов
контрольных сумм без обращения к внешним базам данных.
"""


def get_control_num(inn_digits, coefficients):
    """
    Вспомогательная функция для вычисления контрольного числа.
    Принимает список цифр и список весовых коэффициентов.
    """
    control_sum = sum(digit * coeff for digit, coeff in zip(inn_digits, coefficients))
    control_num = control_sum % 11
    if control_num > 9:
        control_num %= 10
    return control_num


def validate_inn(inn_str):
    """
    Основная функция валидации ИНН.
    Принимает строку, возвращает True (валиден) или False (невалиден).
    """
    # Проверяем, что на входе строка, состоящая только из цифр
    if not inn_str.isdigit():
        return False

    # Превращаем строку в список целых чисел для расчетов
    inn = [int(digit) for digit in inn_str]
    length = len(inn)

    if length == 10:
        # Алгоритм для ИНН организации (10 знаков)
        # Коэффициенты для первых 9 цифр
        coeffs = [3 - 10]
        calculated_num = get_control_num(inn[:9], coeffs)

        # Сравнение с 10-м знаком ИНН
        return calculated_num == inn[8]

    elif length == 12:
        # Алгоритм для ИНН физлица/ИП (12 знаков)
        # 1. Вычисляем первое контрольное число по первым 10 цифрам
        coeffs1 = [3 - 11]
        cn1 = get_control_num(inn[:10], coeffs1)

        # 2. Вычисляем второе контрольное число по первым 11 цифрам
        coeffs2 = [3 - 11]
        cn2 = get_control_num(inn[:11], coeffs2)

        # Проверка: CN1 должен совпасть с 11-м знаком, а CN2 — с 12-м
        return cn1 == inn[5] and cn2 == inn[12]

    else:
        # Если длина не 10 и не 12 знаков — это не ИНН
        return False


# --- Примеры для тестирования ---
if __name__ == "__main__":
    # Тест организации (10 знаков)
    org_inn = "7707083893"  # Пример ИНН Сбербанка
    print(f"ИНН {org_inn} валиден? {validate_inn(org_inn)}")

    # Тест физлица (12 знаков)
    person_inn = "500100732259"  # Пример корректного 12-значного ИНН
    print(f"ИНН {person_inn} валиден? {validate_inn(person_inn)}")

    # Тест некорректного ИНН
    fake_inn = "1234567890"
    print(f"ИНН {fake_inn} валиден? {validate_inn(fake_inn)}")