from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.UserDialog import Ui_UserDialog

class UserDialogEx(Ui_UserDialog):
    def __init__(self, parent=None, user_data=None):
        """user_data: User object if editing, None if creating new"""
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.user_data = user_data
        self.setupSignalAndSlot()
        if user_data:
            self.load_user_data()

    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.validate_and_accept)

    def load_user_data(self):
        self.lineEditFullName.setText(self.user_data.FullName)
        self.lineEditUsername.setText(self.user_data.UserName)
        self.lineEditEmail.setText(self.user_data.Email)
        # Leave password blank (keep current if not entered)
        self.lineEditSecQuestion.setText(self.user_data.SecurityQuestion or "")
        self.lineEditSecAnswer.setText(self.user_data.SecurityAnswer or "")
        # Set role
        idx = self.comboRole.findData(self.user_data.Role)
        if idx >= 0:
            self.comboRole.setCurrentIndex(idx)
        # Do not allow changing own role if necessary (handled in Ex)

    def validate_and_accept(self):
        full_name = self.lineEditFullName.text().strip()
        username  = self.lineEditUsername.text().strip()
        email     = self.lineEditEmail.text().strip()
        password  = self.lineEditPassword.text()

        if not full_name or not username or not email:
            QMessageBox.warning(self.dialog, "Error", "Please fill in full name, username, and email!")
            return
        if not self.user_data and len(password) < 6:
            QMessageBox.warning(self.dialog, "Error", "Password must be at least 6 characters long!")
            return
        if self.user_data and password and len(password) < 6:
            QMessageBox.warning(self.dialog, "Error", "Password must be at least 6 characters long!")
            return
        self.dialog.accept()

    def get_data(self):
        return {
            'full_name':       self.lineEditFullName.text().strip(),
            'username':        self.lineEditUsername.text().strip(),
            'email':           self.lineEditEmail.text().strip(),
            'password':        self.lineEditPassword.text(),   # empty = keep current
            'role':            self.comboRole.currentData(),
            'sec_question':    self.lineEditSecQuestion.text().strip(),
            'sec_answer':      self.lineEditSecAnswer.text().strip().lower()
        }

    def exec(self):
        return self.dialog.exec()