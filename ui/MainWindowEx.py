from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from Event_Check_in_Management.ui.MainWindow import Ui_MainWindow
from Event_Check_in_Management.ui.EventDialogEx import EventDialogEx
from Event_Check_in_Management.ui.AttendeeDialogEx import AttendeeDialogEx
from Event_Check_in_Management.ui.RegistrationDialogEx import RegistrationDialogEx
from Event_Check_in_Management.models.events import Events
from Event_Check_in_Management.models.event import Event
from Event_Check_in_Management.models.attendees import Attendees
from Event_Check_in_Management.models.attendee import Attendee
from Event_Check_in_Management.models.registrations import Registrations
from Event_Check_in_Management.models.registration import Registration
from datetime import datetime
import uuid

try:
    import qrcode
    from PyQt6.QtGui import QPixmap, QImage
    from io import BytesIO
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

class MainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.load_initial_data()
        self.apply_stylesheet()
    
    def showWindow(self):
        self.MainWindow.show()
    
    def setupSignalAndSlot(self):
        """Kết nối các signals với slots"""
        # Tab Sự Kiện
        self.btnAddEvent.clicked.connect(self.add_event)
        self.btnViewEvent.clicked.connect(self.view_event_details)
        self.btnEditEvent.clicked.connect(self.edit_event)
        self.btnDeleteEvent.clicked.connect(self.delete_event)
        self.btnRefreshEvent.clicked.connect(self.load_events)
        
        # Tab Người Tham Dự
        self.attendeeSearch.textChanged.connect(self.search_attendees)
        self.btnAddAttendee.clicked.connect(self.add_attendee)
        self.btnEditAttendee.clicked.connect(self.edit_attendee)
        self.btnDeleteAttendee.clicked.connect(self.delete_attendee)
        self.btnRefreshAttendee.clicked.connect(self.load_attendees)
        
        # Tab Đăng Ký
        self.eventCombo.currentIndexChanged.connect(self.load_registrations)
        self.btnRegisterAttendee.clicked.connect(self.register_attendee)
        self.btnGenerateQR.clicked.connect(self.generate_qr_code)
        self.btnCancelRegistration.clicked.connect(self.cancel_registration)
        self.btnRefreshRegistration.clicked.connect(self.load_registrations)
        
        # Tab Check-in
        self.checkinEventCombo.currentIndexChanged.connect(self.load_checkin_stats)
        self.btnCheckin.clicked.connect(self.perform_checkin)
        self.btnRefreshCheckin.clicked.connect(self.load_checkin_stats)
        
        # Thiết lập header cho các table
        self.eventTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.attendeeTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.registrationTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.checkinTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    def load_initial_data(self):
        """Load dữ liệu ban đầu"""
        self.load_events()
        self.load_attendees()
        self.load_event_combo()
        self.load_checkin_event_combo()
    
    # ===== QUẢN LÝ SỰ KIỆN =====
    def load_events(self):
        """Load danh sách sự kiện"""
        events = Events()
        events.import_json("datasets/events.json")
        
        self.eventTable.setRowCount(len(events.list))
        
        for row, event in enumerate(events.list):
            self.eventTable.setItem(row, 0, QTableWidgetItem(event.EventId))
            self.eventTable.setItem(row, 1, QTableWidgetItem(event.EventName))
            self.eventTable.setItem(row, 2, QTableWidgetItem(event.EventDate))
            self.eventTable.setItem(row, 3, QTableWidgetItem(event.EventTime))
            self.eventTable.setItem(row, 4, QTableWidgetItem(event.Location))
            self.eventTable.setItem(row, 5, QTableWidgetItem(event.Description if event.Description else ""))
    
    def add_event(self):
        """Thêm sự kiện mới"""
        dialog = EventDialogEx(self.MainWindow)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            # Tạo event mới
            event = Event()
            event.EventId = "evt_" + str(uuid.uuid4())[:8]
            event.EventName = data['name']
            event.EventDate = data['date']
            event.EventTime = data['time']
            event.Location = data['location']
            event.Description = data['description']
            
            # Lưu vào file
            events = Events()
            events.import_json("datasets/events.json")
            events.add_item(event)
            events.export_json("datasets/events.json")
            
            QMessageBox.information(self.MainWindow, "Thành Công", "Đã thêm sự kiện mới!")
            self.load_events()
            self.load_event_combo()
            self.load_checkin_event_combo()
    
    def edit_event(self):
        """Sửa sự kiện"""
        current_row = self.eventTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn sự kiện cần sửa!")
            return
        
        event_id = self.eventTable.item(current_row, 0).text()
        
        # Tìm event
        events = Events()
        events.import_json("datasets/events.json")
        event = events.find_event(event_id)
        
        if event:
            dialog = EventDialogEx(self.MainWindow, event)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                
                event.EventName = data['name']
                event.EventDate = data['date']
                event.EventTime = data['time']
                event.Location = data['location']
                event.Description = data['description']
                
                events.export_json("datasets/events.json")
                
                QMessageBox.information(self.MainWindow, "Thành Công", "Đã cập nhật sự kiện!")
                self.load_events()
                self.load_event_combo()
                self.load_checkin_event_combo()
    
    def delete_event(self):
        """Xóa sự kiện"""
        current_row = self.eventTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn sự kiện cần xóa!")
            return
        
        reply = QMessageBox.question(
            self.MainWindow, 
            "Xác Nhận",
            "Bạn có chắc muốn xóa sự kiện này?\nTất cả đăng ký liên quan sẽ bị xóa!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event_id = self.eventTable.item(current_row, 0).text()
            
            # Xóa event
            events = Events()
            events.import_json("datasets/events.json")
            events.delete_event(event_id)
            events.export_json("datasets/events.json")
            
            # Xóa các registrations liên quan
            registrations = Registrations()
            registrations.import_json("datasets/registrations.json")
            registrations.list = [r for r in registrations.list if r.EventId != event_id]
            registrations.export_json("datasets/registrations.json")
            
            QMessageBox.information(self.MainWindow, "Thành Công", "Đã xóa sự kiện!")
            self.load_events()
            self.load_event_combo()
            self.load_checkin_event_combo()
    
    def view_event_details(self):
        """Xem chi tiết sự kiện"""
        current_row = self.eventTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn sự kiện!")
            return
        
        event_id = self.eventTable.item(current_row, 0).text()
        
        events = Events()
        events.import_json("datasets/events.json")
        event = events.find_event(event_id)
        
        if event:
            registrations = Registrations()
            registrations.import_json("datasets/registrations.json")
            
            total_reg = registrations.count_registered_by_event(event_id)
            total_checkin = registrations.count_checkedin_by_event(event_id)
            
            details = f"""
            <h2>{event.EventName}</h2>
            <p><b>📅 Ngày:</b> {event.EventDate}</p>
            <p><b>🕐 Giờ:</b> {event.EventTime}</p>
            <p><b>📍 Địa điểm:</b> {event.Location}</p>
            <p><b>📝 Mô tả:</b> {event.Description if event.Description else 'Không có'}</p>
            <hr>
            <p><b>👥 Tổng đăng ký:</b> {total_reg}</p>
            <p><b>✅ Đã check-in:</b> {total_checkin}</p>
            """
            
            QMessageBox.information(self.MainWindow, "Chi Tiết Sự Kiện", details)
    
    # ===== QUẢN LÝ NGƯỜI THAM DỰ =====
    def load_attendees(self):
        """Load danh sách người tham dự"""
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        
        self.attendeeTable.setRowCount(len(attendees.list))
        
        for row, attendee in enumerate(attendees.list):
            self.attendeeTable.setItem(row, 0, QTableWidgetItem(attendee.AttendeeId))
            self.attendeeTable.setItem(row, 1, QTableWidgetItem(attendee.Name))
            self.attendeeTable.setItem(row, 2, QTableWidgetItem(attendee.Email))
            self.attendeeTable.setItem(row, 3, QTableWidgetItem(attendee.Phone if attendee.Phone else ""))
            self.attendeeTable.setItem(row, 4, QTableWidgetItem(attendee.Organization if attendee.Organization else ""))
            self.attendeeTable.setItem(row, 5, QTableWidgetItem(attendee.Position if attendee.Position else ""))
    
    def search_attendees(self):
        """Tìm kiếm người tham dự"""
        keyword = self.attendeeSearch.text().strip()
        
        if not keyword:
            self.load_attendees()
            return
        
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        results = attendees.search_attendees(keyword)
        
        self.attendeeTable.setRowCount(len(results))
        
        for row, attendee in enumerate(results):
            self.attendeeTable.setItem(row, 0, QTableWidgetItem(attendee.AttendeeId))
            self.attendeeTable.setItem(row, 1, QTableWidgetItem(attendee.Name))
            self.attendeeTable.setItem(row, 2, QTableWidgetItem(attendee.Email))
            self.attendeeTable.setItem(row, 3, QTableWidgetItem(attendee.Phone if attendee.Phone else ""))
            self.attendeeTable.setItem(row, 4, QTableWidgetItem(attendee.Organization if attendee.Organization else ""))
            self.attendeeTable.setItem(row, 5, QTableWidgetItem(attendee.Position if attendee.Position else ""))
    
    def add_attendee(self):
        """Thêm người tham dự mới"""
        dialog = AttendeeDialogEx(self.MainWindow)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            # Kiểm tra email trùng
            attendees = Attendees()
            attendees.import_json("datasets/attendees.json")
            
            for att in attendees.list:
                if att.Email.lower() == data['email'].lower():
                    QMessageBox.warning(self.MainWindow, "Lỗi", "Email đã tồn tại!")
                    return
            
            # Tạo attendee mới
            attendee = Attendee()
            attendee.AttendeeId = "att_" + str(uuid.uuid4())[:8]
            attendee.Name = data['name']
            attendee.Email = data['email']
            attendee.Phone = data['phone']
            attendee.Organization = data['organization']
            attendee.Position = data['position']
            
            attendees.add_item(attendee)
            attendees.export_json("datasets/attendees.json")
            
            QMessageBox.information(self.MainWindow, "Thành Công", "Đã thêm người tham dự!")
            self.load_attendees()
    
    def edit_attendee(self):
        """Sửa người tham dự"""
        current_row = self.attendeeTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn người tham dự cần sửa!")
            return
        
        attendee_id = self.attendeeTable.item(current_row, 0).text()
        
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        attendee = attendees.find_attendee(attendee_id)
        
        if attendee:
            dialog = AttendeeDialogEx(self.MainWindow, attendee)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                
                # Kiểm tra email trùng (trừ chính nó)
                for att in attendees.list:
                    if att.Email.lower() == data['email'].lower() and att.AttendeeId != attendee_id:
                        QMessageBox.warning(self.MainWindow, "Lỗi", "Email đã tồn tại!")
                        return
                
                attendee.Name = data['name']
                attendee.Email = data['email']
                attendee.Phone = data['phone']
                attendee.Organization = data['organization']
                attendee.Position = data['position']
                
                attendees.export_json("datasets/attendees.json")
                
                QMessageBox.information(self.MainWindow, "Thành Công", "Đã cập nhật người tham dự!")
                self.load_attendees()
    
    def delete_attendee(self):
        """Xóa người tham dự"""
        current_row = self.attendeeTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn người tham dự cần xóa!")
            return
        
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác Nhận",
            "Bạn có chắc muốn xóa người tham dự này?\nTất cả đăng ký liên quan sẽ bị xóa!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            attendee_id = self.attendeeTable.item(current_row, 0).text()
            
            attendees = Attendees()
            attendees.import_json("datasets/attendees.json")
            attendees.delete_attendee(attendee_id)
            attendees.export_json("datasets/attendees.json")
            
            # Xóa các registrations liên quan
            registrations = Registrations()
            registrations.import_json("datasets/registrations.json")
            registrations.list = [r for r in registrations.list if r.AttendeeId != attendee_id]
            registrations.export_json("datasets/registrations.json")
            
            QMessageBox.information(self.MainWindow, "Thành Công", "Đã xóa người tham dự!")
            self.load_attendees()
    
    # ===== QUẢN LÝ ĐĂNG KÝ =====
    def load_event_combo(self):
        """Load combo box sự kiện"""
        self.eventCombo.clear()
        events = Events()
        events.import_json("datasets/events.json")
        
        for event in events.list:
            self.eventCombo.addItem(f"{event.EventName} - {event.EventDate}", event.EventId)
    
    def load_registrations(self):
        """Load danh sách đăng ký"""
        if self.eventCombo.count() == 0:
            self.registrationTable.setRowCount(0)
            return
        
        event_id = self.eventCombo.currentData()
        if not event_id:
            return
        
        registrations = Registrations()
        registrations.import_json("datasets/registrations.json")
        regs = registrations.get_registrations_by_event(event_id)
        
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        
        self.registrationTable.setRowCount(len(regs))
        
        for row, reg in enumerate(regs):
            attendee = attendees.find_attendee(reg.AttendeeId)
            if attendee:
                self.registrationTable.setItem(row, 0, QTableWidgetItem(reg.RegistrationId))
                self.registrationTable.setItem(row, 1, QTableWidgetItem(attendee.Name))
                self.registrationTable.setItem(row, 2, QTableWidgetItem(attendee.Email))
                self.registrationTable.setItem(row, 3, QTableWidgetItem(attendee.Organization if attendee.Organization else ""))
                self.registrationTable.setItem(row, 4, QTableWidgetItem(reg.RegistrationDate))
                self.registrationTable.setItem(row, 5, QTableWidgetItem(reg.Status))
    
    def register_attendee(self):
        """Đăng ký người tham dự vào sự kiện"""
        if self.eventCombo.count() == 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không có sự kiện nào!")
            return
        
        event_id = self.eventCombo.currentData()
        if not event_id:
            return
        
        dialog = RegistrationDialogEx(self.MainWindow)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            attendee_id = dialog.get_selected_attendee_id()
            
            if not attendee_id:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn người tham dự!")
                return
            
            # Kiểm tra đã đăng ký chưa
            registrations = Registrations()
            registrations.import_json("datasets/registrations.json")
            
            existing = registrations.find_registration_by_event_attendee(event_id, attendee_id)
            if existing:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Người này đã đăng ký sự kiện!")
                return
            
            # Tạo registration mới
            reg = Registration()
            reg.RegistrationId = str(uuid.uuid4())[:8].upper()
            reg.EventId = event_id
            reg.AttendeeId = attendee_id
            reg.RegistrationDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reg.Status = "Đã đăng ký"
            
            registrations.add_item(reg)
            registrations.export_json("datasets/registrations.json")
            
            QMessageBox.information(self.MainWindow, "Thành Công", f"Đã đăng ký!\nMã đăng ký: {reg.RegistrationId}")
            self.load_registrations()
    
    def cancel_registration(self):
        """Hủy đăng ký"""
        current_row = self.registrationTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn đăng ký cần hủy!")
            return
        
        reply = QMessageBox.question(
            self.MainWindow,
            "Xác Nhận",
            "Bạn có chắc muốn hủy đăng ký này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            reg_id = self.registrationTable.item(current_row, 0).text()
            
            registrations = Registrations()
            registrations.import_json("datasets/registrations.json")
            registrations.delete_registration(reg_id)
            registrations.export_json("datasets/registrations.json")
            
            QMessageBox.information(self.MainWindow, "Thành Công", "Đã hủy đăng ký!")
            self.load_registrations()
    
    def generate_qr_code(self):
        """Tạo mã QR cho đăng ký"""
        if not QR_AVAILABLE:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Chưa cài đặt thư viện qrcode!\nCài đặt: pip install qrcode[pil]")
            return
        
        current_row = self.registrationTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn đăng ký!")
            return
        
        reg_id = self.registrationTable.item(current_row, 0).text()
        attendee_name = self.registrationTable.item(current_row, 1).text()
        
        # Tạo QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(reg_id)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Chuyển đổi sang QPixmap
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        qimage = QImage()
        qimage.loadFromData(buffer.read())
        pixmap = QPixmap.fromImage(qimage)
        
        # Hiển thị dialog với QR code
        qr_dialog = QDialog(self.MainWindow)
        qr_dialog.setWindowTitle("Mã QR Check-in")
        qr_dialog.resize(400, 450)
        
        qr_layout = QVBoxLayout()
        
        qr_label = QLabel()
        qr_label.setPixmap(pixmap)
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        code_label = QLabel(f"<h3>{attendee_name}</h3><h2>Mã: {reg_id}</h2>")
        code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        qr_layout.addWidget(qr_label)
        qr_layout.addWidget(code_label)
        
        qr_dialog.setLayout(qr_layout)
        qr_dialog.exec()
    
    # ===== CHECK-IN =====
    def load_checkin_event_combo(self):
        """Load combo box sự kiện cho check-in"""
        self.checkinEventCombo.clear()
        events = Events()
        events.import_json("datasets/events.json")
        
        for event in events.list:
            self.checkinEventCombo.addItem(f"{event.EventName} - {event.EventDate}", event.EventId)
    
    def load_checkin_stats(self):
        """Load thống kê check-in"""
        if self.checkinEventCombo.count() == 0:
            self.totalRegisteredLabel.setText("0")
            self.totalCheckedinLabel.setText("0")
            self.checkinTable.setRowCount(0)
            return
        
        event_id = self.checkinEventCombo.currentData()
        if not event_id:
            return
        
        registrations = Registrations()
        registrations.import_json("datasets/registrations.json")
        
        total_reg = registrations.count_registered_by_event(event_id)
        total_checkin = registrations.count_checkedin_by_event(event_id)
        
        self.totalRegisteredLabel.setText(str(total_reg))
        self.totalCheckedinLabel.setText(str(total_checkin))
        
        # Load danh sách đã check-in
        regs = registrations.get_registrations_by_event(event_id)
        checkedin = [r for r in regs if r.Status == "Đã check-in"]
        
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        
        self.checkinTable.setRowCount(len(checkedin))
        
        for row, reg in enumerate(checkedin):
            attendee = attendees.find_attendee(reg.AttendeeId)
            if attendee:
                self.checkinTable.setItem(row, 0, QTableWidgetItem(attendee.Name))
                self.checkinTable.setItem(row, 1, QTableWidgetItem(attendee.Email))
                self.checkinTable.setItem(row, 2, QTableWidgetItem(attendee.Organization if attendee.Organization else ""))
                self.checkinTable.setItem(row, 3, QTableWidgetItem(reg.CheckinTime if reg.CheckinTime else ""))
                self.checkinTable.setItem(row, 4, QTableWidgetItem(reg.RegistrationId))
    
    def perform_checkin(self):
        """Thực hiện check-in"""
        code = self.checkinCode.text().strip().upper()
        
        if not code:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập mã đăng ký!")
            return
        
        registrations = Registrations()
        registrations.import_json("datasets/registrations.json")
        
        success, message = registrations.checkin(code)
        
        if success:
            registrations.export_json("datasets/registrations.json")
            QMessageBox.information(self.MainWindow, "Thành Công", message)
            self.checkinCode.clear()
            self.load_checkin_stats()
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", message)
    
    def apply_stylesheet(self):
        """Áp dụng stylesheet cho ứng dụng"""
        self.MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                background-color: white;
            }
        """)
