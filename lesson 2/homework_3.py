"""
Задание №3
Описание: Математические расчеты и генератор процессуальных документов.
Реализовано: факториал, поиск максимума, площадь треугольника
и автоматическая генерация шапки документа.
"""

import math

# --- Часть 1: Математические функции ---

def calculate_factorial(n):
    """Вычисляет факториал числа n (произведение от 1 до n)."""
    if n < 0:
        return "Ошибка: число должно быть положительным"
    return math.factorial(n)

def find_max_of_three(numbers):
    """Принимает кортеж из трех чисел и возвращает наибольшее из них."""
    return max(numbers)

def calculate_triangle_area(a, b):
    """Рассчитывает площадь прямоугольного треугольника по двум катетам."""
    return 0.5 * a * b


# --- Часть 2: Генерация текста документа ---

# Справочник арбитражных судов (согласно заданию)
COURTS_REGISTRY = {
    "А40": {
        "name": "Арбитражный суд города Москвы",
        "address": "115225, г. Москва, ул. Б. Тульская, 17"
    },
    "А41": {
        "name": "Арбитражный суд Московской области",
        "address": "107053, г. Москва, проспект Академика Сахарова, д.18"
    }
}

def generate_document_header(defendant_data, case_number):
    """
    Генерирует шапку процессуального документа.
    """
    # case_number.split('-') возвращает список: ['А40', '123456/2023']
    parts = case_number.split('-')

    # Берем индекс , чтобы получить строку 'А40'
    # Без  court_code будет списком, что вызовет ошибку TypeError
    court_code = parts[0]

    # Теперь .get() получит строку и успешно найдет данные в словаре
    court = COURTS_REGISTRY.get(court_code, {
        "name": "Неизвестный суд",
        "address": "Адрес не найден"
    })

    # Данные истца (подставьте свои данные согласно заданию)
    plaintiff = {
        "name": "Шахмамедов Рауль",
        "inn": "770011223344",
        "ogrnip": "318774600123456",
        "address": "123456, г. Москва, ул. Ленина, д. 1"
    }

    # Формирование шаблона через f-string [5]
    header = (
        f"В {court['name']}\n"
        f"Адрес: {court['address']}\n\n"
        f"Истец: {plaintiff['name']}\n"
        f"ИНН {plaintiff['inn']} ОГРНИП {plaintiff['ogrnip']}\n"
        f"Адрес: {plaintiff['address']}\n\n"
        f"Ответчик: {defendant_data['name']}\n"
        f"ИНН {defendant_data['inn']} ОГРН {defendant_data['ogrn']}\n"
        f"Адрес: {defendant_data['address']}\n\n"
        f"Номер дела {case_number}"
    )
    return header

def batch_generate_headers(defendants_list):
    """Генерирует шапки для списка словарей с данными ответчиков."""
    for item in defendants_list:
        header = generate_document_header(item['defendant'], item['case_number'])
        print("-" * 40)
        print(header)
        print("-" * 40)

# --- Пример запуска для проверки ---

# 1. Проверка математики
print(f"Факториал 5: {calculate_factorial(5)}")
print(f"Максимум из (10, 50, 20): {find_max_of_three((10, 50, 20))}")
print(f"Площадь треугольника (3, 4): {calculate_triangle_area(3, 4)}")

# 2. Проверка генератора
sample_data = [
    {
        "case_number": "А40-123456/2023",
        "defendant": {
            "name": "ООО 'Кооператив Озеро'",
            "inn": "1231231231",
            "ogrn": "123124129312941",
            "address": "123534, г. Москва, ул. Красивых молдавских партизан, 69"
        }
    }
]

batch_generate_headers(sample_data)