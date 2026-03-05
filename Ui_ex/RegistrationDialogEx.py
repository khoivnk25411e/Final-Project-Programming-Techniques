from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.RegistrationDialog import Ui_RegistrationDialog

from models.attendees import Attendees
from models.registrations import Registrations


class RegistrationDialogEx(Ui_RegistrationDialog):
    def __init__(self, parent=None, event_id=None):
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.event_id = event_id
        self.setupSignalAndSlot()
        self.load_attendees()

    def setupSignalAndSlot(self):
        self.btnRegister.clicked.connect(self.validate_and_accept)

    def load_attendees(self):
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")

        registered_ids = set()
        if self.event_id:
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            for reg in regs.get_registrations_by_event(self.event_id):
                registered_ids.add(reg.AttendeeId)

        available = [a for a in attendees.list if a.AttendeeId not in registered_ids]

        self.attendeeCombo.clear()
        for attendee in available:
            self.attendeeCombo.addItem(
                f"{attendee.Name} - {attendee.Email}",
                attendee.AttendeeId
            )

        if not available:
            self.btnRegister.setEnabled(False)
            self.attendeeCombo.addItem("⚠️ All attendees have already registered for this event")

    def validate_and_accept(self):
        if self.attendeeCombo.currentData() is None:
            QMessageBox.warning(
                self.dialog,
                "Error",
                "No attendee available to register!"
            )
            return
        self.dialog.accept()

    def get_selected_attendee_id(self):
        return self.attendeeCombo.currentData()

    def exec(self):
        return self.dialog.exec()