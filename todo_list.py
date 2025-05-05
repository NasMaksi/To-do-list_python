import json
import os

FILE_NAME = "tasks.json"

def get_input(prompt):
    """Функция для ввода данных"""
    return input(prompt)

def show_output(message):
    """Функция для вывода данных"""
    print(message)

def load_tasks():
    """Загрузка задач из файла"""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_tasks(tasks):
    """Сохранение задач в файл"""
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

def add_task(tasks):
    """Добавление новой задачи"""
    task = get_input("Введите задачу: ")
    tasks.append({"task": task, "done": False})
    show_output("Задача добавлена!")
    save_tasks(tasks)  # Явное сохранение после изменения

def view_tasks(tasks):
    """Просмотр списка задач"""
    if not tasks:
        show_output("Список задач пуст.")
    else:
        show_output("Список задач:")
        for i, task in enumerate(tasks, 1):
            status = "✓" if task["done"] else " "
            show_output(f"{i}. [{status}] {task['task']}")

def mark_done(tasks):
    """Отметка задачи как выполненной"""
    view_tasks(tasks)
    try:
        num = int(get_input("Номер задачи для отметки: ")) - 1
        if 0 <= num < len(tasks):
            tasks[num]["done"] = True
            show_output("Задача отмечена выполненной!")
            save_tasks(tasks)
        else:
            show_output("Неверный номер задачи.")
    except ValueError:
        show_output("Введите число!")

def delete_task(tasks):
    """Удаление задачи"""
    view_tasks(tasks)
    try:
        num = int(get_input("Номер задачи для удаления: ")) - 1
        if 0 <= num < len(tasks):
            deleted = tasks.pop(num)
            show_output(f"Задача '{deleted['task']}' удалена!")
            save_tasks(tasks)
        else:
            show_output("Неверный номер задачи.")
    except ValueError:
        show_output("Введите число!")

def main():
    """Основной цикл программы"""
    tasks = load_tasks()
    while True:
        show_output("\nОрганайзер задач")
        show_output("1. Добавить задачу")
        show_output("2. Просмотреть задачи")
        show_output("3. Отметить задачу выполненной")
        show_output("4. Удалить задачу")
        show_output("5. Выход")

        choice = get_input("Выберите действие: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            show_output("Данные сохранены. До свидания!")
            break
        else:
            show_output("Неверный ввод!")

if __name__ == "__main__":
    main()