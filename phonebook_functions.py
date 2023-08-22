import sqlite3
import re


def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id INTEGER PRIMARY KEY,
        last_name TEXT,
        first_name TEXT,
        middle_name TEXT,
        organization TEXT,
        work_phone TEXT,
        personal_phone TEXT
    )
    """
    conn.execute(query)

def display_page(conn, page_num, page_size):
    start_idx = (page_num - 1) * page_size
    query = f"SELECT * FROM phonebook LIMIT {page_size} OFFSET {start_idx}"
    cursor = conn.execute(query)
    for row in cursor:
        print(row)

def validate_phone_number(phone_number):
    # Паттерн для валидации номера телефона (например, 7XXXXXXXXXX)
    pattern = r'^7\d{10}$'
    return re.match(pattern, phone_number) is not None


def add_entry(conn):
    last_name = input("Введите фамилию: ")
    first_name = input("Введите имя: ")
    middle_name = input("Введите отчество: ")
    organization = input("Введите название организации: ")

    work_phone = input("Введите рабочий телефон (в формате 7XXXXXXXXXX): ")
    if not validate_phone_number(work_phone):
        print("Некорректный формат рабочего телефона.")
        return

    personal_phone = input("Введите личный телефон (в формате  7XXXXXXXXXX): ")
    if personal_phone and not validate_phone_number(personal_phone):
        print("Некорректный формат личного телефона.")
        return

    data = (last_name, first_name, middle_name, organization, work_phone, personal_phone)
    query = "INSERT INTO phonebook (last_name, first_name, middle_name, organization, work_phone, personal_phone) VALUES (?, ?, ?, ?, ?, ?)"
    conn.execute(query, data)
    conn.commit()


def edit_entry(conn, entry_id):
    query = "SELECT * FROM phonebook WHERE id = ?"
    cursor = conn.execute(query, (entry_id,))
    entry = cursor.fetchone()

    if not entry:
        print("Запись с указанным ID не найдена.")
        return

    print("Текущая запись:")
    print(entry)

    print("Выберите поле для редактирования:")
    print("1. Фамилия")
    print("2. Имя")
    print("3. Отчество")
    print("4. Название организации")
    print("5. Рабочий телефон")
    print("6. Личный телефон")
    field_choice = int(input("Введите номер поля: "))

    field_names = ["last_name", "first_name", "middle_name", "organization", "work_phone", "personal_phone"]
    selected_field = field_names[field_choice - 1]

    new_value = input(f"Введите новое значение для {selected_field}: ")
    query = f"UPDATE phonebook SET {selected_field} = ? WHERE id = ?"
    conn.execute(query, (new_value, entry_id))
    conn.commit()

    print("Запись успешно обновлена.")


def search_entries(conn, query):
    search_pattern = '%' + query + '%'
    query = "SELECT * FROM phonebook WHERE last_name LIKE ? OR first_name LIKE ? OR organization LIKE ?"
    cursor = conn.execute(query, (search_pattern, search_pattern, search_pattern))
    results = cursor.fetchall()
    return results



def delete_entry(conn, entry_id):
    query = "DELETE FROM phonebook WHERE id = ?"
    conn.execute(query, (entry_id,))
    conn.commit()
