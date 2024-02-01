import dataclasses
from enum import Enum
import json
from datetime import datetime
import argparse
import os.path as osp

class TaskStatus(int,Enum):
    NEW = 1
    IN_PROGRESS = 2
    IN_REVIEW = 3
    DONE = 4
    CANCELED = 5


@dataclasses.dataclass
class Task:
    name: str
    description: str
    status: TaskStatus = TaskStatus.NEW
    creation_date: datetime = dataclasses.field(default_factory=lambda: datetime.now())
    status_change_date: datetime = dataclasses.field(default_factory=lambda: datetime.now())

    def to_dict(self):
        return dataclasses.asdict(self)

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.history = []

    def add_task(self, task):
        self.tasks.append(task)
        self.history.append(f"Добавлена задача {task.name}")
        print(f"{task.name} id is {len(self.tasks)-1}")

    def change_status(self, task, new_status):
        if new_status == TaskStatus.CANCELED:
            task.status = new_status
        elif new_status.value == task.status.value + 1 or new_status.value == task.status.value - 1:
            task.status = new_status
            task.status_change_date = datetime.now()
        else:
            print("Невозможно изменить статус таким образом")

        self.history.append(f"Изменен статус задачи {task.name} на {new_status.value}")

    def save_to_file(self, file_name):
        data = {"tasks": [t.to_dict() for t in self.tasks],
                "history": self.history}
        with open(file_name, "w") as f:
            json.dump(data, f, default=str)

    def load_from_file(self, file_name):
        if osp.exists("./"+file_name):
            with open(file_name) as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data["tasks"]]
                self.history = data["history"]
        else:
            print("File doesn't exist")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks")
    args = parser.parse_args()

    manager = TaskManager()
    manager.load_from_file(args.tasks)

    while True:
        print("Выберите действие:")
        print("1 - Добавить задачу")
        print("2 - Изменить статус задачи")
        print("3 - Просмотреть задачи")
        print("4 - Просмотреть историю")
        print("5 - Сохранить")
        print("6 - Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            name = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            task = Task(name=name, description=description)
            manager.add_task(task)
        elif choice == "2":
            task_id = int(input("Введите id задачи: "))
            try:
                task = manager.tasks[task_id]
            except IndexError:
                print("Неверный id")
                continue
            new_status = TaskStatus[input("Введите новый статус: ")]
            manager.change_status(task, new_status)
        elif choice == "3":
            print("Список задач:")
            for i, task in enumerate(manager.tasks):
                print(f"{i}. {task.name} - {task.status.name}")
        elif choice == "4":
            print("История:")
            for record in manager.history:
                print(record)
        elif choice == "5":
            manager.save_to_file(args.tasks)
            print("Данные сохранены в файл")
        elif choice == "6":
            break
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()
