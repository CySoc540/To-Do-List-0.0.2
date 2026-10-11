from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QVBoxLayout,
                              QWidget, QPushButton, QListWidget,
                              QLabel, QHBoxLayout, QApplication, QSpinBox)
from PyQt5.QtCore import Qt

from todolist_backend import add_task, complete_task, remove_task, fetch_all_tasks, truncate_table


class ToDoWindow (QMainWindow):
    def __init__(self):
        super ().__init__()
        self.task_input = QLineEdit ()
        self.priority_input = QSpinBox ()
        self.priority_input.setRange (1, 3)
        self.comment_input = QLineEdit ()


        self.root_layout = QVBoxLayout ()
        self.container = QWidget ()
        self.setContentsMargins (10, 10, 10, 10)
        self.setGeometry(300, 300, 1000, 800)


        self.container.setLayout (self.root_layout)
        self.setCentralWidget(self.container)
        self.add_button = QPushButton ("Add Task")
        self.add_button.clicked.connect(self.on_add_task)
        self.task_list = QListWidget ()
        self.setWindowTitle ("To-Do List")

        self.complete_task_button = QPushButton ("Complete Task")
        self.complete_task_button.clicked.connect(self.on_complete_task_button)

        self.delete_button = QPushButton ("Delete Task")
        self.delete_button.clicked.connect(self.on_delete_task)

        self.clear_button = QPushButton ("Clear All Tasks")
        self.clear_button.clicked.connect(self.on_clear_button)

        self.root_layout.addWidget(self.task_input)
        self.task_input.setPlaceholderText ("Task Name")
        self.root_layout.addWidget(self.priority_input)
        self.priority_input.setAccessibleDescription("Priority")
        self.root_layout.addWidget (self.comment_input)
        self.comment_input.setPlaceholderText ("Comment")
        self.root_layout.addWidget (self.add_button)
        self.root_layout.addWidget (self.task_list)
        self.root_layout.addWidget (self.complete_task_button)
        self.root_layout.addWidget (self.delete_button)
        self.root_layout.addWidget (self.clear_button)
        self.refresh_tasks()
        self.root_layout.addStretch ()

    def refresh_tasks(self):
        self.task_list.clear()
        tasks = fetch_all_tasks()
        for task in tasks:
            task_name, finished, priority, comment = task
            status = "Done" if finished else "Not Done"
            priority_label = {1: "High", 2: "Medium", 3: "Low"}.get(priority, "?")
            self.task_list.addItem(f"{priority_label} [{status}] {task_name}")

    def on_add_task(self):
        task_text = self.task_input.text()
        priority = self.priority_input.value()
        comment = self.comment_input.text()

        add_task(task_text, priority, comment)

        self.task_input.clear()
        self.comment_input.clear()

        self.refresh_tasks()
        self.task_input.setFocus ()

    def on_complete_task_button(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            display_text = item.text()
            task_name = display_text.split("] ", 1)[1]

            complete_task (task_name)
            self.refresh_tasks()
        else:
            print ("No task selected")

    def on_delete_task(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            display_text = selected_task.text()
            task_name = display_text.split("] ", 1)[1]
            remove_task(task_name)
            self.refresh_tasks()
        else:
            print ("No task selected")

    def on_clear_button(self):
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, "Confirm",
            "Clear ALL Tasks?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            truncate_table()
            self.refresh_tasks()
            print ("Tasks Cleared Successfully")
        else:
            print ("Tasks Not Cleared")