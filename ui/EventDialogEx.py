from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import QDate, QTime
from Event_Check_in_Management.ui.EventDialog import Ui_EventDialog

class EventDialogEx(Ui_EventDialog):
    def __init__(self, parent=None, event_data=None):
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.event_data = event_data
        self.setupSignalAndSlot()
        
        if event_data:
            self.load_event_data()
        else:
            self.dateInput.setDate(QDate.currentDate())
            self.timeInput.setTime(QTime.currentTime())
    
    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.validate_and_accept)
    
    def load_event_data(self):
        """Load dữ liệu sự kiện để sửa"""
        self.nameInput.setText(self.event_data.EventName)
        
        # Parse date DD/MM/YYYY
        date_parts = self.event_data.EventDate.split('/')
        self.dateInput.setDate(QDate(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])))
        
        # Parse time HH:MM
        time_parts = self.event_data.EventTime.split(':')
        self.timeInput.setTime(QTime(int(time_parts[0]), int(time_parts[1])))
        
        self.locationInput.setText(self.event_data.Location)
        self.descriptionInput.setText(self.event_data.Description if self.event_data.Description else "")
    
    def validate_and_accept(self):
        """Kiểm tra dữ liệu trước khi chấp nhận"""
        if not self.nameInput.text().strip() or not self.locationInput.text().strip():
            QMessageBox.warning(self.dialog, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        self.dialog.accept()
    
    def get_data(self):
        """Lấy dữ liệu từ form"""
        return {
            'name': self.nameInput.text().strip(),
            'date': self.dateInput.date().toString("dd/MM/yyyy"),
            'time': self.timeInput.time().toString("HH:mm"),
            'location': self.locationInput.text().strip(),
            'description': self.descriptionInput.toPlainText().strip()
        }
    
    def exec(self):
        return self.dialog.exec()
