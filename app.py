import sys
from PyQt5.QtWidgets import QApplication
from gui.teacher import TeacherWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherWidget()
    window.show()
    sys.exit(app.exec_())
