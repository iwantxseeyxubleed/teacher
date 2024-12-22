from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableView, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class TeacherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Management")
        self.setGeometry(100, 100, 800, 600)
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("school.db")
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", self.db.lastError().text())

        self.initUI()
        self.load_data()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject")
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_teacher)
        
        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_teacher)
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_teacher)
        
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.subject_input)
        form_layout.addWidget(add_button)
        form_layout.addWidget(update_button)
        form_layout.addWidget(delete_button)
        
        self.table_view = QTableView()
        self.table_view.clicked.connect(self.on_row_clicked)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.table_view)
        
        self.setLayout(layout)

    def load_data(self):
        self.model = QSqlTableModel()
        self.model.setTable("Teachers")
        self.model.select()
        self.table_view.setModel(self.model)

    def on_row_clicked(self, index):
        self.selected_row = index.row()
        self.name_input.setText(self.model.index(self.selected_row, 1).data())
        self.subject_input.setText(self.model.index(self.selected_row, 2).data())

    def add_teacher(self):
        name = self.name_input.text()
        subject = self.subject_input.text()
        
        if name and subject:
            row = self.model.rowCount()
            self.model.insertRow(row)
            self.model.setData(self.model.index(row, 1), name)
            self.model.setData(self.model.index(row, 2), subject)
            if self.model.submitAll():
                QMessageBox.information(self, "Success", "Teacher added successfully")
                self.name_input.clear()
                self.subject_input.clear()
            else:
                QMessageBox.critical(self, "Error", "Failed to add teacher")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both name and subject")

    def update_teacher(self):
        if hasattr(self, 'selected_row'):
            name = self.name_input.text()
            subject = self.subject_input.text()
            
            if name and subject:
                self.model.setData(self.model.index(self.selected_row, 1), name)
                self.model.setData(self.model.index(self.selected_row, 2), subject)
                if self.model.submitAll():
                    QMessageBox.information(self, "Success", "Teacher updated successfully")
                    self.name_input.clear()
                    self.subject_input.clear()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update teacher")
            else:
                QMessageBox.warning(self, "Input Error", "Please enter both name and subject")

    def delete_teacher(self):
        if hasattr(self, 'selected_row'):
            self.model.removeRow(self.selected_row)
            if self.model.submitAll():
                QMessageBox.information(self, "Success", "Teacher deleted successfully")
                self.name_input.clear()
                self.subject_input.clear()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete teacher")
