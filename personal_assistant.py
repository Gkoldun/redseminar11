import os
import json
import csv
from datetime import datetime

class Notes:
    def __init__(self, id, title, content, timestamp):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Notes(
            id=data['id'],
            title=data['title'],
            content=data['content'],
            timestamp=data['timestamp']
        )

class Tasks:
    def __init__(self, id, short_description, long_description, finished, priority, deadline):
        self.id = id
        self.short_description = short_description
        self.long_description = long_description
        self.finished = finished
        self.priority = priority
        self.deadline = deadline

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.short_description,
            'description': self.long_description,
            'done': self.finished,
            'priority': self.priority,
            'due_date': self.deadline
        }

    @staticmethod
    def from_dict(data):
        return Tasks(
            id=data['id'],
            short_description=data['title'],
            long_description=data['description'],
            finished=data['done'],
            priority=data['priority'],
            deadline=data['due_date']
        )

class Contacts:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    @staticmethod
    def from_dict(data):
        return Contacts(
            id=data['id'],
            name=data['name'],
            phone=data['phone'],
            email=data['email']
        )

class FinanceRecord:
    def __init__(self, id, amount, category, date, description):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

    @staticmethod
    def from_dict(data):
        return FinanceRecord(
            id=data['id'],
            amount=data['amount'],
            category=data['category'],
            date=data['date'],
            description=data['description']
        )

def start_app():
    while True:
        print("\nПерсональный Ассистент")
        print("1. Заметки")
        print("2. Задачи")
        print("3. Контакты")
        print("4. Финансы")
        print("5. Калькулятор")
        print("6. Завершить работу")
        action = input("Выберите номер действия: ")

        if action == '1':
            notes_interface()
        elif action == '2':
            tasks_interface()
        elif action == '3':
            contacts_interface()
        elif action == '4':
            finance_interface()
        elif action == '5':
            run_calculator()
        elif action == '6':
            print("Приложение завершено. Благодарим за использование!")
            break
        else:
            print("Неверный ввод. Повторите попытку.")

def load_notes():
    if not os.path.exists('notes_data.json'):
        return []
    with open('notes_data.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
        return [Notes.from_dict(m) for m in content]

def save_notes(notes_list):
    with open('notes_data.json', 'w', encoding='utf-8') as f:
        json.dump([m.to_dict() for m in notes_list], f, ensure_ascii=False, indent=4)

def notes_interface():
    while True:
        print("\nУправление заметками")
        print("1. Создать заметку")
        print("2. Просмотреть все заметки")
        print("3. Подробный просмотр заметки")
        print("4. Обновить заметку")
        print("5. Удалить заметку")
        print("6. Импорт из CSV")
        print("7. Экспорт в CSV")
        print("8. Вернуться назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            create_note()
        elif choice == '2':
            show_all_notes()
        elif choice == '3':
            show_single_note()
        elif choice == '4':
            update_notes()
        elif choice == '5':
            remove_note()
        elif choice == '6':
            import_notes_csv()
        elif choice == '7':
            export_notes_csv()
        elif choice == '8':
            break
        else:
            print("Неверный ввод. Повторите попытку.")

def create_note():
    all_notes = load_notes()
    new_id = max((m.id for m in all_notes), default=0) + 1
    title = input("Введите заголовок: ").strip()
    if not title:
        print("Заголовок не может быть пустым.")
        return
    text = input("Введите содержимое: ")
    now_stamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    new_note = Notes(new_id, title, text, now_stamp)
    all_notes.append(new_note)
    save_notes(all_notes)
    print("Заметка добавлена.")

def show_all_notes():
    notes_list = load_notes()
    if not notes_list:
        print("Нет ни одной заметки.")
        return
    print("\nСписок заметок:")
    for m in notes_list:
        print(f"ID: {m.id}, Заголовок: {m.title}, Дата: {m.timestamp}")

def show_single_note():
    note_id = input("Введите ID заметки: ")
    notes_list = load_notes()
    for m in notes_list:
        if str(m.id) == note_id:
            print(f"\nЗаголовок: {m.title}")
            print(f"Содержимое: {m.content}")
            print(f"Дата: {m.timestamp}")
            return
    print("Заметка не найдена.")

def update_notes():
    note_id = input("Введите ID заметки для изменения: ")
    notes_list = load_notes()
    for m in notes_list:
        if str(m.id) == note_id:
            new_title = input(f"Новый заголовок (старый: {m.title}): ").strip()
            if not new_title:
                print("Заголовок не может быть пустым.")
                return
            new_text = input("Новое содержимое: ")
            new_stamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            m.title = new_title
            m.content = new_text
            m.timestamp = new_stamp
            save_notes(notes_list)
            print("Заметка обновлена.")
            return
    print("Заметка не найдена.")

def remove_note():
    note_id = input("Введите ID для удаления: ")
    notes_list = load_notes()
    updated_notes = [m for m in notes_list if str(m.id) != note_id]
    save_notes(updated_notes)
    print("Заметка удалена.")

def import_notes_csv():
    file_name = input("Укажите CSV-файл для импорта: ")
    try:
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            readr = csv.DictReader(csv_file)
            existing = load_notes()
            for row in readr:
                imported = Notes(
                    id=int(row['id']),
                    title=row['title'],
                    content=row['content'],
                    timestamp=row['timestamp']
                )
                existing.append(imported)
            save_notes(existing)
            print("Импорт завершен.")
    except Exception as e:
        print(f"Ошибка импорта: {e}")

def export_notes_csv():
    file_name = input("Укажите CSV-файл для экспорта: ")
    notes_list = load_notes()
    if not notes_list:
        print("Нет заметок для экспорта.")
        return
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        fields = ['id', 'title', 'content', 'timestamp']
        writr = csv.DictWriter(csv_file, fieldnames=fields)
        writr.writeheader()
        for m in notes_list:
            writr.writerow(m.to_dict())
    print("Экспорт завершен.")


def load_tasks():
    if not os.path.exists('tasks_data.json'):
        return []
    with open('tasks_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Tasks.from_dict(j) for j in data]

def save_tasks(tasks):
    with open('tasks_data.json', 'w', encoding='utf-8') as f:
        json.dump([j.to_dict() for j in tasks], f, ensure_ascii=False, indent=4)

def tasks_interface():
    while True:
        print("\nУправление задачами")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Отметить задачу выполненной")
        print("4. Изменить задачу")
        print("5. Удалить задачу")
        print("6. Импорт задач из CSV")
        print("7. Экспорт задач в CSV")
        print("8. Фильтр задач")
        print("9. Вернуться назад")
        ch = input("Выберите номер: ")

        if ch == '1':
            add_task()
        elif ch == '2':
            display_tasks()
        elif ch == '3':
            finish_task()
        elif ch == '4':
            modify_task()
        elif ch == '5':
            delete_task()
        elif ch == '6':
            import_tasks_csv()
        elif ch == '7':
            export_tasks_csv()
        elif ch == '8':
            filter_tasks()
        elif ch == '9':
            break
        else:
            print("Неверный ввод.")

def add_task():
    tasks_list = load_tasks()
    new_id = max((j.id for j in tasks_list), default=0) + 1
    title = input("Название задачи: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    desc = input("Подробности задачи: ")
    priority = input("Приоритет (Высокий/Средний/Низкий): ")
    if priority not in ['Высокий', 'Средний', 'Низкий']:
        print("Некорректный приоритет. Установлен по умолчанию: Средний.")
        priority = 'Средний'
    due = input("Срок (ДД-ММ-ГГГГ): ")
    try:
        datetime.strptime(due, '%d-%m-%Y')
    except ValueError:
        print("Неверный формат даты.")
        return
    new_task = Tasks(new_id, title, desc, False, priority, due)
    tasks_list.append(new_task)
    save_tasks(tasks_list)
    print("Задача добавлена.")

def display_tasks():
    tasks_list = load_tasks()
    if not tasks_list:
        print("Нет задач.")
        return
    print("\nСписок задач:")
    for task in tasks_list:
        status = "Выполнена" if task.finished else "Не выполнена"
        print(f"ID: {task.id}, Название: {task.short_description}, Статус: {status}, Приоритет: {task.priority}, Срок: {task.deadline}")

def finish_task():
    task_id = input("ID задачи для отметки выполненной: ")
    tasks_list = load_tasks()
    for task in tasks_list:
        if str(task.id) == task_id:
            task.finished = True
            save_tasks(tasks_list)
            print("Отмечена как выполненная.")
            return
    print("Задача не найдена.")

def modify_task():
    task_id = input("ID задачи для изменения: ")
    tasks_list = load_tasks()
    for task in tasks_list:
        if str(task.id) == task_id:
            new_title = input(f"Новое название (старое: {task.short_description}): ")
            if not new_title:
                print("Название не может быть пустым.")
                return
            task.short_description = new_title
            task.long_description = input("Новое описание: ")
            new_priority = input(f"Новый приоритет (старый: {task.priority}): ")
            if new_priority in ['Высокий', 'Средний', 'Низкий']:
                task.priority = new_priority
            else:
                print("Приоритет не изменен из-за неверного ввода.")
            new_due = input(f"Новый срок (старый: {task.deadline}): ")
            try:
                datetime.strptime(new_due, '%d-%m-%Y')
                task.deadline = new_due
            except ValueError:
                print("Дата не изменена (неверный формат).")
            save_tasks(tasks_list)
            print("Задача обновлена.")
            return
    print("Задача не найдена.")

def delete_task():
    task_id = input("ID задачи для удаления: ")
    tasks_list = load_tasks()
    filtered_tasks = [task for task in tasks_list if str(task.id) != task_id]
    save_tasks(filtered_tasks)
    print("Задача удалена.")

def import_tasks_csv():
    file_name = input("CSV-файл для импорта: ")
    try:
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            readr = csv.DictReader(csv_file)
            exist = load_tasks()
            for row in readr:
                task = Tasks(
                    id=int(row['id']),
                    short_description=row['title'],
                    long_description=row['description'],
                    finished=(row['done'] == 'True'),
                    priority=row['priority'],
                    deadline=row['due_date']
                )
                exist.append(task)
            save_tasks(exist)
            print("Импорт завершен.")
    except Exception as e:
        print(f"Ошибка импорта: {e}")

def export_tasks_csv():
    file_name = input("CSV-файл для экспорта: ")
    tasks_list = load_tasks()
    if not tasks_list:
        print("Нет задач для экспорта.")
        return
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        fn = ['id','title','description','done','priority','due_date']
        writr = csv.DictWriter(csv_file, fieldnames=fn)
        writr.writeheader()
        for task in tasks_list:
            writr.writerow(task.to_dict())
    print("Экспорт завершен.")

def filter_tasks():
    print("\nФильтры для задач:")
    print("1. По статусу")
    print("2. По приоритету")
    print("3. По сроку")
    choice = input("Выберите фильтр: ")
    tasks_list = load_tasks()
    if not tasks_list:
        print("Нет задач.")
        return
    if choice == '1':
        st = input("Статус (Выполнена/Не выполнена): ")
        desired = True if st == 'Выполнена' else False
        subset = [task for task in tasks_list if task.finished == desired]
    elif choice == '2':
        pr = input("Приоритет (Высокий/Средний/Низкий): ")
        subset = [task for task in tasks_list if task.priority == pr]
    elif choice == '3':
        dd = input("Срок (ДД-ММ-ГГГГ): ")
        subset = [task for task in tasks_list if task.deadline == dd]
    else:
        print("Неправильный выбор.")
        return

    if not subset:
        print("Ничего не найдено по заданным критериям.")
        return
    for task in subset:
        st = "Выполнена" if task.finished else "Не выполнена"
        print(f"ID: {task.id}, Название: {task.short_description}, Статус: {st}, Приоритет: {task.priority}, Срок: {task.deadline}")

def load_contacts():
    if not os.path.exists('contacts_data.json'):
        return []
    with open('contacts_data.json', 'r', encoding='utf-8') as f:
        arr = json.load(f)
        return [Contacts.from_dict(p) for p in arr]

def save_contacts(contacts_list):
    with open('contacts_data.json', 'w', encoding='utf-8') as f:
        json.dump([contact.to_dict() for contact in contacts_list], f, ensure_ascii=False, indent=4)

def contacts_interface():
    while True:
        print("\nУправление контактами")
        print("1. Добавить контакт")
        print("2. Поиск контактов")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Импорт из CSV")
        print("6. Экспорт в CSV")
        print("7. Назад")
        ch = input("Выберите действие: ")
        if ch == '1':
            add_contact()
        elif ch == '2':
            find_contact()
        elif ch == '3':
            modify_contact()
        elif ch == '4':
            remove_contact()
        elif ch == '5':
            import_contacts_csv()
        elif ch == '6':
            export_contacts_csv()
        elif ch == '7':
            break
        else:
            print("Неверный ввод.")

def add_contact():
    contacts_list = load_contacts()
    new_id = max((contact.id for contact in contacts_list), default=0) + 1
    name = input("Введите имя: ").strip()
    if not name:
        print("Имя не может быть пустым.")
        return
    phone = input("Телефон: ")
    email = input("Email: ")
    new_contact = Contacts(new_id, name, phone, email)
    contacts_list.append(new_contact)
    save_contacts(contacts_list)
    print("Контакт добавлен.")

def find_contact():
    q = input("Введите имя или телефон для поиска: ").strip()
    contacts_list = load_contacts()
    matches = [contact for contact in contacts_list if q.lower() in contact.name.lower() or q in contact.phone]
    if not matches:
        print("Контакты не найдены.")
        return
    print("\nНайденные контакты:")
    for contact in matches:
        print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")

def modify_contact():
    contact_id = input("ID контакта для изменения: ")
    contacts_list = load_contacts()
    for contact in contacts_list:
        if str(contact.id) == contact_id:
            new_name = input(f"Новое имя (старое: {contact.name}): ").strip()
            if not new_name:
                print("Имя не может быть пустым.")
                return
            new_phone = input(f"Новый телефон (старый: {contact.phone}): ")
            new_mail = input(f"Новый email (старый: {contact.email}): ")
            contact.name = new_name
            contact.phone = new_phone
            contact.email = new_mail
            save_contacts(contacts_list)
            print("Контакт обновлен.")
            return
    print("Контакт не найден.")

def remove_contact():
    contact_id = input("ID для удаления: ")
    contacts_list = load_contacts()
    filtered_contacts = [contact for contact in contacts_list if str(contact.id) != contact_id]
    save_contacts(filtered_contacts)
    print("Контакт удален.")

def import_contacts_csv():
    file_name = input("CSV-файл для импорта: ")
    try:
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            readr = csv.DictReader(csv_file)
            existing = load_contacts()
            for row in readr:
                contact = Contacts(
                    id=int(row['id']),
                    name=row['name'],
                    phone=row['phone'],
                    email=row['email']
                )
                existing.append(contact)
            save_contacts(existing)
            print("Импорт контактов завершен.")
    except Exception as e:
        print(f"Ошибка импорта: {e}")

def export_contacts_csv():
    file_name = input("CSV-файл для экспорта: ")
    contacts_list = load_contacts()
    if not contacts_list:
        print("Нет контактов для экспорта.")
        return
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        fn = ['id','name','phone','email']
        writr = csv.DictWriter(csv_file, fieldnames=fn)
        writr.writeheader()
        for contact in contacts_list:
            writr.writerow(contact.to_dict())
    print("Экспорт завершен.")

def load_finance():
    if not os.path.exists('finance_data.json'):
        return []
    with open('finance_data.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        return [FinanceRecord.from_dict(rec) for rec in raw_data]

def save_finance(records):
    with open('finance_data.json', 'w', encoding='utf-8') as f:
        json.dump([record.to_dict() for record in records], f, ensure_ascii=False, indent=4)

def finance_interface():
    while True:
        print("\nФинансовые операции")
        print("1. Добавить операцию")
        print("2. Просмотр операций")
        print("3. Отчёт за период")
        print("4. Подсчёт общего баланса")
        print("5. Импорт из CSV")
        print("6. Экспорт в CSV")
        print("7. Назад")
        ch = input("Выберите действие: ")
        if ch == '1':
            add_finance_record()
        elif ch == '2':
            show_finance_records()
        elif ch == '3':
            generate_finance_report()
        elif ch == '4':
            calc_total_balance()
        elif ch == '5':
            import_finance_csv()
        elif ch == '6':
            export_finance_csv()
        elif ch == '7':
            break
        else:
            print("Неверный ввод.")

def add_finance_record():
    existing = load_finance()
    new_id = max((record.id for record in existing), default=0) + 1
    val = input("Сумма операции (+ доход, - расход): ")
    try:
        val = float(val)
    except ValueError:
        print("Некорректная сумма.")
        return
    category = input("Категория: ")
    date = input("Дата (ДД-ММ-ГГГГ): ")
    try:
        datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        print("Неверный формат даты.")
        return
    info = input("Описание: ")
    record = FinanceRecord(new_id, val, category, date, info)
    existing.append(record)
    save_finance(existing)
    print("Операция добавлена.")

def show_finance_records():
    records_list = load_finance()
    if not records_list:
        print("Нет записей.")
        return
    print("\nФинансовые записи:")
    for record in records_list:
        print(f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")

def generate_finance_report():
    start = input("Начальная дата (ДД-ММ-ГГГГ): ")
    end = input("Конечная дата (ДД-ММ-ГГГГ): ")
    try:
        start_date = datetime.strptime(start, '%d-%m-%Y')
        end_date = datetime.strptime(end, '%d-%m-%Y')
    except ValueError:
        print("Неверный формат даты.")
        return
    records_list = load_finance()
    filtered_records = [record for record in records_list if start_date <= datetime.strptime(record.date, '%d-%m-%Y') <= end_date]
    if not filtered_records:
        print("Нет данных за период.")
        return
    total_income = sum(record.amount for record in filtered_records if record.amount > 0)
    total_expense = sum(record.amount for record in filtered_records if record.amount < 0)
    print(f"\nОтчет с {start} по {end}:")
    print(f"Доход: {total_income}")
    print(f"Расход: {total_expense}")
    print(f"Итоговый баланс: {total_income + total_expense}")

def calc_total_balance():
    recs = load_finance()
    balance = sum(record.amount for record in recs)
    print(f"Текущий баланс: {balance}")

def import_finance_csv():
    file_name = input("CSV-файл для импорта: ")
    try:
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            readr = csv.DictReader(csv_file)
            existing = load_finance()
            for row in readr:
                new_record = FinanceRecord(
                    id=int(row['id']),
                    amount=float(row['amount']),
                    category=row['category'],
                    date=row['date'],
                    description=row['description']
                )
                existing.append(new_record)
            save_finance(existing)
            print("Импорт выполнен.")
    except Exception as e:
        print(f"Ошибка: {e}")

def export_finance_csv():
    file_name = input("CSV-файл для экспорта: ")
    records_list = load_finance()
    if not records_list:
        print("Нет данных для экспорта.")
        return
    with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
        fn = ['id','amount','category','date','description']
        writr = csv.DictWriter(csv_file, fieldnames=fn)
        writr.writeheader()
        for record in records_list:
            writr.writerow(record.to_dict())
    print("Экспорт выполнен.")

def run_calculator():
    print("\nКалькулятор")
    expr = input("Введите выражение: ")
    try:
        valid_chars = set('0123456789+-*/(). ')
        if not set(expr).issubset(valid_chars):
            raise ValueError("Недопустимые символы в выражении.")
        result = eval(expr, {"__builtins__": None}, {})
        print("Результат:", result)
    except ZeroDivisionError:
        print("Ошибка: деление на ноль.")
    except Exception as e:
        print(f"Ошибка в выражении: {e}")

if __name__ == "__main__":
    start_app()