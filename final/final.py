import json
from datetime import datetime

# --- ШАГ 1: Загрузка данных ---
try:
    with open('bankruptcy_messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)

    with open('organizations.json', 'r', encoding='utf-8') as f:
        org_list = json.load(f)

    priority_case_numbers = []
    with open('priority_cases.txt', 'r', encoding='utf-8') as f:
        for line in f:
            case_num = line.strip()
            if case_num:
                priority_case_numbers.append(case_num)

    print(f"✅ Данные загружены. Сообщений: {len(messages)}, Организаций: {len(org_list)}")

except FileNotFoundError as e:
    print(f"❌ Ошибка: Файл не найден! Проверьте, что файл {e.filename} лежит в папке со скриптом.")
    exit()

# Реестр организаций
org_registry = {org['inn']: org for org in org_list}

# --- Шаг 2: Валидация ---
valid_messages = []
validation_errors = []
error_stats = {}

for msg in messages:
    errors = []
    inn = msg.get('publisher_inn')

    # Проверка ИНН
    if not inn:
        errors.append("missing_inn")
    elif inn not in org_registry:
        errors.append("inn_not_found_in_registry")

    # Проверка даты
    date_str = msg.get('date_published')
    parsed_date = None

    if not date_str:
        errors.append("missing_date")
    else:
        for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except (ValueError, TypeError):
                continue

        if not parsed_date:
            errors.append("invalid_date_format")

    # Распределение
    if errors:
        validation_errors.append({
            "case_number": msg.get('case_number', 'Unknown'),
            "errors": errors,
            "raw_data": msg
        })
        for err_type in errors:
            error_stats[err_type] = error_stats.get(err_type, 0) + 1
    else:
        org_info = org_registry[inn]
        msg['org_name'] = org_info['name']
        msg['region'] = org_info['region']
        msg['date_published'] = parsed_date.strftime("%Y-%m-%d")
        valid_messages.append(msg)

print(f"✅ Обработка завершена.")
print(f"Валидных сообщений: {len(valid_messages)}")
print(f"Ошибок: {len(validation_errors)}")
print(f"Статистика ошибок: {error_stats}")

# --- ШАГ 3: Приоритетные дела ---
priority_set = set(priority_case_numbers)
message_case_set = set([msg['case_number'] for msg in valid_messages if msg.get('case_number')])
priority_found = priority_set & message_case_set

print(f"Найдено приоритетных дел в текущей выгрузке: {len(priority_found)}")

# --- Шаг 3.1: Извлечение сумм ---
def extract_amounts(text):
    if not text:
        return []

    amounts = []
    words = text.split()

    for i, word in enumerate(words):
        if "руб" in word:
            num_parts = []
            j = i - 1

            while j >= 0 and words[j].replace(" ", "").isdigit():
                num_parts.insert(0, words[j])
                j -= 1

            if num_parts:
                amount = " ".join(num_parts)

                if j >= 0 and words[j] in ["тыс.", "млн"]:
                    amount = amount + " " + words[j]

                amount += " руб."
                amounts.append(amount)

    return amounts

# применяем
for msg in valid_messages:
    msg["amounts"] = extract_amounts(msg.get("msg_text"))

# проверка
print(valid_messages[0]["amounts"])

# ✅ дополнительная проверка
print("\nПример извлечённых сумм:")
for msg in valid_messages[:3]:
    print(msg["amounts"])

# --- Шаг 3.2: Аналитика ---
def normalize_amount(amount_str):
    if not amount_str:
        return 0

    parts = amount_str.replace("руб.", "").split()
    multiplier = 1

    if "тыс." in parts:
        multiplier = 1_000
        parts.remove("тыс.")
    elif "млн" in parts:
        multiplier = 1_000_000
        parts.remove("млн")

    number = "".join(parts)

    if number.isdigit():
        return int(number) * multiplier

    return 0

# считаем суммы
for msg in valid_messages:
    amounts = msg.get("amounts", [])
    numeric_amounts = [normalize_amount(a) for a in amounts]
    msg["total_amount"] = sum(numeric_amounts)

# общая сумма
total_sum = sum(msg.get("total_amount", 0) for msg in valid_messages)

print(f"\n📊 Общая сумма по всем сообщениям: {total_sum:,} руб.")

# группировка по регионам
region_stats = {}

for msg in valid_messages:
    region = msg.get("region", "Unknown")
    amount = msg.get("total_amount", 0)
    region_stats[region] = region_stats.get(region, 0) + amount

print("\n📍 Суммы по регионам:")
for region, amount in sorted(region_stats.items(), key=lambda x: x[1], reverse=True):  # ✅ сортировка
    print(f"{region}: {amount:,} руб.")

# топ-5 дел
top_cases = sorted(
    valid_messages,
    key=lambda x: x.get("total_amount", 0),
    reverse=True
)[:5]

print("\n🏆 ТОП-5 дел по сумме:")
for case in top_cases:
    print(f"{case.get('case_number')} | {case.get('total_amount'):,} руб. | {case.get('org_name')}")

# финальный вывод
print("\n📌 Вывод:")
print(f"Общая сумма задолженности: {total_sum:,} руб.")
print("Наибольшая финансовая нагрузка сосредоточена в ограниченном числе дел.")
print("Это указывает на высокую концентрацию рисков.")
print("Рекомендуется уделить внимание крупнейшим делам и регионам с максимальными суммами.")