from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.ForgotPasswordDialog import Ui_ForgotPasswordDialog
from models.users import Users


class ForgotPasswordDialogEx(Ui_ForgotPasswordDialog):
    def __init__(self, parent=None):
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self._found_user = None
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        self.btnVerifyUser.clicked.connect(self.verify_username)
        self.btnConfirm.clicked.connect(self.reset_password)

    def verify_username(self):

        username = self.lineEditUsername.text().strip()
        if not username:
            QMessageBox.warning(self.dialog, "Error", "Please enter your username!")
            return

        users = Users()
        users.import_json("datasets/users.json")
        user = users.find_by_username(username)

        if user is None:
            QMessageBox.warning(self.dialog, "Error", "Username does not exist!")
            return

        if not user.SecurityQuestion:
            QMessageBox.warning(
                self.dialog,
                "Error",
                "This account has not set up a security question!"
            )
            return

        self._found_user = user


        self.lblQuestionText.setText(user.SecurityQuestion)
        self.lblQuestion.setVisible(True)
        self.lblQuestionText.setVisible(True)
        self.lblAnswer.setVisible(True)
        self.lineEditAnswer.setVisible(True)
        self.btnConfirm.setVisible(True)


        self.lineEditUsername.setEnabled(False)
        self.btnVerifyUser.setEnabled(False)

        self.dialog.setFixedSize(420, 400)

    def reset_password(self):

        answer = self.lineEditAnswer.text().strip().lower()
        if not answer:
            QMessageBox.warning(self.dialog, "Error", "Please enter your answer!")
            return

        if answer != self._found_user.SecurityAnswer.lower():
            QMessageBox.warning(self.dialog, "Incorrect", "The answer is incorrect!")
            return

        self.dialog.accept()

    def get_user(self):
        return self._found_user

    def exec(self):
        return self.dialog.exec()