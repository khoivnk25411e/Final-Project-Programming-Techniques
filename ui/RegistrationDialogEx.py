from PyQt6.QtWidgets import QDialog
from Event_Check_in_Management.ui.RegistrationDialog import Ui_RegistrationDialog

from Event_Check_in_Management.models.attendees import Attendees


class RegistrationDialogEx(Ui_RegistrationDialog):
    def __init__(self, parent=None):
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.setupSignalAndSlot()
        self.load_attendees()
    
    def setupSignalAndSlot(self):
        self.btnRegister.clicked.connect(self.dialog.accept)
    
    def load_attendees(self):
        """Load danh sách người tham dự vào combo box"""
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        
        for attendee in attendees.list:
            self.attendeeCombo.addItem(f"{attendee.Name} - {attendee.Email}", attendee.AttendeeId)
    
    def get_selected_attendee_id(self):
        """Lấy ID người tham dự được chọn"""
        return self.attendeeCombo.currentData()
    
    def exec(self):
        return self.dialog.exec()
