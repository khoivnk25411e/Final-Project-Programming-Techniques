from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit

from Event_Check_in_Management.ui.ChangePasswordDialog import Ui_ChangePasswordDialog
from Event_Check_in_Management.models.users import Users


class ChangePasswordDialogEx(Ui_ChangePasswordDialog):
    def __init__(self, parent=None, current_user=None, skip_old_password=False):

        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.current_user = current_user
        self.skip_old_password = skip_old_password
        self.setupSignalAndSlot()
        self._init_form()

    def _init_form(self):
        if self.current_user:
            self.lblUser.setText(
                f"Account: {self.current_user.FullName} ({self.current_user.UserName})"
            )

        if self.skip_old_password:

            self.lblOldPwd.setVisible(False)
            self.lineEditOldPwd.setVisible(False)
            self.btnToggleOld.setVisible(False)
            self.dialog.setFixedSize(400, 280)

    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.process_change)
        self.btnToggleOld.clicked.connect(
            lambda: self._toggle_echo(self.lineEditOldPwd)
        )
        self.btnToggleNew.clicked.connect(
            lambda: self._toggle_echo(self.lineEditNewPwd)
        )

    def _toggle_echo(self, field):
        if field.echoMode() == QLineEdit.EchoMode.Password:
            field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            field.setEchoMode(QLineEdit.EchoMode.Password)

    def process_change(self):
        new_pwd = self.lineEditNewPwd.text()
        confirm = self.lineEditConfirmPwd.text()


        if not self.skip_old_password:
            old_pwd = self.lineEditOldPwd.text()
            if not old_pwd:
                QMessageBox.warning(
                    self.dialog, "Error", "Please enter your current password!"
                )
                return
            if old_pwd != self.current_user.Password:
                QMessageBox.warning(
                    self.dialog, "Incorrect", "Current password is incorrect!"
                )
                return

        if len(new_pwd) < 6:
            QMessageBox.warning(
                self.dialog, "Error", "New password must be at least 6 characters!"
            )
            return

        if new_pwd != confirm:
            QMessageBox.warning(
                self.dialog, "Error", "Password confirmation does not match!"
            )
            return

        if not self.skip_old_password and new_pwd == self.current_user.Password:
            QMessageBox.warning(
                self.dialog, "Error", "New password must be different from old password!"
            )
            return

        # Save new password
        users = Users()
        users.import_json("datasets/users.json")
        user = users.find_user(self.current_user.UserId)

        if user:
            user.Password = new_pwd
            users.export_json("datasets/users.json")
            # Update in-memory object
            self.current_user.Password = new_pwd

        QMessageBox.information(
            self.dialog, "Success", "Password changed successfully!"
        )
        self.dialog.accept()

    def exec(self):
        return self.dialog.exec()