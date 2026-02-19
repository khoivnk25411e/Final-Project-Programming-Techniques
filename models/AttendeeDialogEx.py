from PyQt6.QtWidgets import QMessageBox, QDialog
from Event_Check_in_Management.ui.AttendeeDialog import Ui_AttendeeDialog

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
        """Load dữ liệu người tham dự để sửa"""
        self.nameInput.setText(self.attendee_data.Name)
        self.emailInput.setText(self.attendee_data.Email)
        self.phoneInput.setText(self.attendee_data.Phone if self.attendee_data.Phone else "")
        self.organizationInput.setText(self.attendee_data.Organization if self.attendee_data.Organization else "")
        self.positionInput.setText(self.attendee_data.Position if self.attendee_data.Position else "")
    
    def validate_and_accept(self):
        """Kiểm tra dữ liệu trước khi chấp nhận"""
        if not self.nameInput.text().strip() or not self.emailInput.text().strip():
            QMessageBox.warning(self.dialog, "Lỗi", "Vui lòng điền họ tên và email!")
            return
        self.dialog.accept()
    
    def get_data(self):
        """Lấy dữ liệu từ form"""
        return {
            'name': self.nameInput.text().strip(),
            'email': self.emailInput.text().strip(),
            'phone': self.phoneInput.text().strip(),
            'organization': self.organizationInput.text().strip(),
            'position': self.positionInput.text().strip()
        }
    
    def exec(self):
        return self.dialog.exec()
