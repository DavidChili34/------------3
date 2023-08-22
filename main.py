import sqlite3
from phonebook_functions import *

def main():
    conn = sqlite3.connect("phonebook.db")
    create_table(conn)

    while True:
        print("1. Вывод записей")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Удаление записи")
        print("5. Поиск записей")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            page_num = int(input("Введите номер страницы: "))
            page_size = 10
            display_page(conn, page_num, page_size)
        elif choice == "2":
            add_entry(conn)
        elif choice == "3":
            entry_id = int(input("Введите ID записи для редактирования: "))
            edit_entry(conn, entry_id)
        elif choice == "4":
            entry_id = int(input("Введите ID записи для удаления: "))
            delete_entry(conn, entry_id)
        elif choice == "5":
            query = input("Введите текст для поиска: ")
            results = search_entries(conn, query)
            for result in results:
                print(result)
        elif choice == "6":
            break
        else:
            print("Недопустимый выбор")

    conn.close()
    save_to_text_file(conn, "phonebook.txt")
 

def save_to_text_file(conn,filename):
    with open(filename, "w") as file:
        conn = sqlite3.connect("phonebook.db")
        cursor = conn.execute("SELECT * FROM phonebook")
        for row in cursor:
            file.write(" ".join(map(str, row)) + "\n")
        conn.close()


if __name__ == "__main__":
    main()
