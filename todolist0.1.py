import PyQt5
from PyQt5.QtWidgets import QApplication
import todolist_frontend
import sys

app = QApplication(sys.argv)
window = todolist_frontend.ToDoWindow ()
window.show()
sys.exit(app.exec_())