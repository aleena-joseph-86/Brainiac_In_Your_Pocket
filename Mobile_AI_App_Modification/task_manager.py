import json

class TaskManager:
    def __init__(self, dataset='dataset.json'):
        self.dataset = dataset
        self.load_tasks()

    def load_tasks(self):
        with open(self.dataset, 'r') as file:
            data = json.load(file)
            self.tasks = data.get('tasks', [])

    def save_tasks(self):
        with open(self.dataset, 'w') as file:
            json.dump({"tasks": self.tasks}, file)

    def add_task(self, task):
        self.tasks.append({"task": task, "completed": False})
        self.save_tasks()
        return f"Task '{task}' added successfully."

    def remove_task(self, task):
        for t in self.tasks:
            if t["task"] == task:
                self.tasks.remove(t)
                self.save_tasks()
                return f"Task '{task}' removed successfully."
        return f"Task '{task}' not found."

    def complete_task(self, task):
        for t in self.tasks:
            if t["task"] == task:
                t["completed"] = True
                self.save_tasks()
                return f"Task '{task}' marked as completed."
        return f"Task '{task}' not found."

    def show_tasks(self):
        if not self.tasks:
            return "No tasks available."
        tasks_str = "\n".join([f"{t['task']} (Completed)" if t['completed'] else t['task'] for t in self.tasks])
        return tasks_str

