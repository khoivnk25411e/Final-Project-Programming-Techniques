import re
from PyQt6.QtWidgets import QMessageBox, QDialog
from ui.AttendeeDialog import Ui_AttendeeDialog


class AttendeeDialogEx(Ui_AttendeeDialog):
    def __init__(self, parent=None, attendee_data=None):
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.attendee_data = attendee_data
        self.setupSignalAndSlot()
        if attendee_data:
            self.load_attendee_data()

    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.validate_and_accept)

    def load_attendee_data(self):
        self.nameInput.setText(self.attendee_data.Name)
        self.emailInput.setText(self.attendee_data.Email)
        self.phoneInput.setText(self.attendee_data.Phone if self.attendee_data.Phone else "")
        self.organizationInput.setText(self.attendee_data.Organization if self.attendee_data.Organization else "")
        self.positionInput.setText(self.attendee_data.Position if self.attendee_data.Position else "")

    def validate_and_accept(self):
        name  = self.nameInput.text().strip()
        email = self.emailInput.text().strip()
        phone = self.phoneInput.text().strip()

        if not name or not email:
            QMessageBox.warning(self.dialog, "Error", "Please fill in full name and email!")
            return

        if not re.match(r'^[\w.+-]+@[\w-]+\.[\w.]+$', email):
            QMessageBox.warning(self.dialog, "Invalid Email",
                                "Email format is invalid!\nExample: name@example.com")
            return

        if phone and not re.match(r'^[+]?[0-9]{9,15}$',
                                  phone.replace(' ', '').replace('-', '')):
            QMessageBox.warning(self.dialog, "Invalid Phone",
                                "Phone number is invalid!\nExample: 0901234567")
            return

        self.dialog.accept()

    def get_data(self):
        return {
            'name':         self.nameInput.text().strip(),
            'email':        self.emailInput.text().strip(),
            'phone':        self.phoneInput.text().strip(),
            'organization': self.organizationInput.text().strip(),
            'position':     self.positionInput.text().strip()
        }

    def exec(self):
        return self.dialog.exec()