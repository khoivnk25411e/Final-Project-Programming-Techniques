from PyQt6.QtWidgets import (QMessageBox, QTableWidgetItem, QHeaderView,
                             QDialog, QVBoxLayout, QLabel, QMainWindow)
from PyQt6.QtCore import Qt, QTimer
from ui.MainWindow import Ui_MainWindow
from UI_Ex.EventDialogEx import EventDialogEx
from UI_Ex.AttendeeDialogEx import AttendeeDialogEx
from UI_Ex.ChangePasswordDialogEx import ChangePasswordDialogEx
from models.events import Events
from models.event import Event
from models.attendees import Attendees
from models.attendee import Attendee
from models.registrations import Registrations
from models.registration import Registration
from models.users import Users
from models.user import User
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
        self._apply_role_ui()
        self.setupSignalAndSlot()
        self.load_initial_data()
        self.apply_stylesheet()

    def showWindow(self):
        self.MainWindow.show()

    def _apply_role_ui(self):
        user = getattr(self, 'login_user', None)
        if user is None:
            return

        is_admin = (user.Role == "admin")

        self.lblLoginUser.setText(f"👤  {user.FullName}  ({user.UserName})")
        if is_admin:
            self.lblRoleBadge.setText("ADMIN")
            self.lblRoleBadge.setStyleSheet(
                "QLabel{background:#e74c3c;color:white;border-radius:5px;"
                "font-size:11px;font-weight:bold;padding:0 8px;}"
            )
        else:
            self.lblRoleBadge.setText("USER")

        idx = self.tabWidget.indexOf(self.userMgmtTab)
        if not is_admin and idx >= 0:
            self.tabWidget.removeTab(idx)

        if not is_admin:
            self.btnAddEvent.setEnabled(False)
            self.btnDeleteEvent.setEnabled(False)
            self.btnAddAttendee.setEnabled(False)
            self.btnDeleteAttendee.setEnabled(False)
            self.btnCheckin.setEnabled(False)
            self.btnScanQR.setEnabled(False)
            self.checkinCode.setEnabled(False)
            self.checkinCode.setPlaceholderText("Only Admin can Check-in")

    def setupSignalAndSlot(self):
        self.btnChangePassword.clicked.connect(self.change_password)
        self.btnLogout.clicked.connect(self.logout)

        self.btnAddEvent.clicked.connect(self.add_event)
        self.btnViewEvent.clicked.connect(self.view_event_details)
        self.btnEditEvent.clicked.connect(self.edit_event)
        self.btnDeleteEvent.clicked.connect(self.delete_event)
        self.btnRefreshEvent.clicked.connect(self.load_events)

        self.attendeeSearch.textChanged.connect(self.search_attendees)
        self.btnAddAttendee.clicked.connect(self.add_attendee)
        self.btnEditAttendee.clicked.connect(self.edit_attendee)
        self.btnDeleteAttendee.clicked.connect(self.delete_attendee)
        self.btnRefreshAttendee.clicked.connect(self.load_attendees)

        self.eventCombo.currentIndexChanged.connect(self.load_registrations)
        self.btnRegisterAttendee.clicked.connect(self.register_attendee)
        self.btnGenerateQR.clicked.connect(self.generate_qr_code)
        self.btnCancelRegistration.clicked.connect(self.cancel_registration)
        self.btnRefreshRegistration.clicked.connect(self.load_registrations)

        self.checkinEventCombo.currentIndexChanged.connect(self.load_checkin_stats)
        self.btnCheckin.clicked.connect(self.perform_checkin)
        self.btnScanQR.clicked.connect(self.scan_qr_checkin)
        self.btnRefreshCheckin.clicked.connect(self.load_checkin_stats)

        user = getattr(self, 'login_user', None)
        if user and user.Role == "admin":
            self.btnAddUser.clicked.connect(self.add_user)
            self.btnEditUser.clicked.connect(self.edit_user)
            self.btnDeleteUser.clicked.connect(self.delete_user)
            self.btnResetUserPwd.clicked.connect(self.reset_user_password)
            self.btnRefreshUser.clicked.connect(self.load_users)

        for tbl in [self.eventTable, self.attendeeTable,
                    self.registrationTable, self.checkinTable]:
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        if user and user.Role == "admin":
            self.userTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_initial_data(self):
        self.load_events()
        self.load_attendees()
        self.load_event_combo()
        self.load_checkin_event_combo()
        user = getattr(self, 'login_user', None)
        if user and user.Role == "admin":
            self.load_users()

    def change_password(self):
        user = getattr(self, 'login_user', None)
        if not user:
            return
        dlg = ChangePasswordDialogEx(self.MainWindow, current_user=user, skip_old_password=False)
        dlg.exec()

    def logout(self):
        reply = QMessageBox.question(
            self.MainWindow, "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.MainWindow.close()
            from UI_Ex.LoginWindowEx import LoginWindowEx
            self.login_gui = LoginWindowEx()
            self.login_gui.setupUi(QMainWindow())
            self.login_gui.showWindow()

    def load_users(self):
        users = Users()
        users.import_json("datasets/users.json")
        self.userTable.setRowCount(len(users.list))
        for row, u in enumerate(users.list):
            self.userTable.setItem(row, 0, QTableWidgetItem(u.UserId))
            self.userTable.setItem(row, 1, QTableWidgetItem(u.FullName))
            self.userTable.setItem(row, 2, QTableWidgetItem(u.UserName))
            self.userTable.setItem(row, 3, QTableWidgetItem(u.Email))
            role_text = "🔑 Admin" if u.Role == "admin" else "👤 User"
            self.userTable.setItem(row, 4, QTableWidgetItem(role_text))

    def add_user(self):
        dlg = UserDialogEx(self.MainWindow)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            users = Users()
            users.import_json("datasets/users.json")

            if users.find_by_username(data['username']):
                QMessageBox.warning(self.MainWindow, "Error", "Username already exists!")
                return
            if users.find_by_email(data['email']):
                QMessageBox.warning(self.MainWindow, "Error", "Email already exists!")
                return

            new_user = User()
            new_user.UserId = "usr_" + str(uuid.uuid4())[:8]
            new_user.FullName = data['full_name']
            new_user.UserName = data['username']
            new_user.Password = data['password']
            new_user.Email = data['email']
            new_user.Role = data['role']
            new_user.SecurityQuestion = data['sec_question']
            new_user.SecurityAnswer = data['sec_answer']

            users.add_item(new_user)
            users.export_json("datasets/users.json")
            QMessageBox.information(self.MainWindow, "Success", "New account added!")
            self.load_users()

    def edit_user(self):
        row = self.userTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an account to edit!")
            return
        user_id = self.userTable.item(row, 0).text()
        users = Users()
        users.import_json("datasets/users.json")
        user = users.find_user(user_id)
        if not user:
            return

        dlg = UserDialogEx(self.MainWindow, user_data=user)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()

            existing_un = users.find_by_username(data['username'])
            if existing_un and existing_un.UserId != user_id:
                QMessageBox.warning(self.MainWindow, "Error", "Username already exists!")
                return
            existing_em = users.find_by_email(data['email'])
            if existing_em and existing_em.UserId != user_id:
                QMessageBox.warning(self.MainWindow, "Error", "Email already exists!")
                return

            user.FullName = data['full_name']
            user.UserName = data['username']
            user.Email = data['email']
            if data['password']:
                user.Password = data['password']
            user.Role = data['role']
            user.SecurityQuestion = data['sec_question']
            user.SecurityAnswer = data['sec_answer']

            users.export_json("datasets/users.json")
            QMessageBox.information(self.MainWindow, "Success", "Account updated!")
            self.load_users()

    def delete_user(self):
        row = self.userTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an account to delete!")
            return
        user_id = self.userTable.item(row, 0).text()

        if getattr(self, 'login_user', None) and self.login_user.UserId == user_id:
            QMessageBox.warning(self.MainWindow, "Error", "Cannot delete the currently logged-in account!")
            return

        reply = QMessageBox.question(
            self.MainWindow, "Confirm", "Are you sure you want to delete this account?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            users = Users()
            users.import_json("datasets/users.json")
            users.delete_user(user_id)
            users.export_json("datasets/users.json")
            QMessageBox.information(self.MainWindow, "Success", "Account deleted!")
            self.load_users()

    def reset_user_password(self):
        row = self.userTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an account!")
            return
        user_id = self.userTable.item(row, 0).text()
        users = Users()
        users.import_json("datasets/users.json")
        user = users.find_user(user_id)
        if user:
            dlg = ChangePasswordDialogEx(self.MainWindow, current_user=user, skip_old_password=True)
            dlg.exec()

    def load_events(self):
        events = Events()
        events.import_json("datasets/events.json")
        self.eventTable.setRowCount(len(events.list))
        for row, event in enumerate(events.list):
            self.eventTable.setItem(row, 0, QTableWidgetItem(event.EventId))
            self.eventTable.setItem(row, 1, QTableWidgetItem(event.EventName))
            self.eventTable.setItem(row, 2, QTableWidgetItem(event.EventDate))
            self.eventTable.setItem(row, 3, QTableWidgetItem(event.EventTime))
            self.eventTable.setItem(row, 4, QTableWidgetItem(event.Location))
            self.eventTable.setItem(row, 5, QTableWidgetItem(event.Description or ""))

    def add_event(self):
        dlg = EventDialogEx(self.MainWindow)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            event = Event()
            event.EventId = "evt_" + str(uuid.uuid4())[:8]
            event.EventName = data['name']
            event.EventDate = data['date']
            event.EventTime = data['time']
            event.Location = data['location']
            event.Description = data['description']
            events = Events()
            events.import_json("datasets/events.json")
            events.add_item(event)
            events.export_json("datasets/events.json")
            QMessageBox.information(self.MainWindow, "Success", "New event added!")
            self.load_events()
            self.load_event_combo()
            self.load_checkin_event_combo()

    def edit_event(self):
        row = self.eventTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an event to edit!")
            return
        event_id = self.eventTable.item(row, 0).text()
        events = Events()
        events.import_json("datasets/events.json")
        event = events.find_event(event_id)
        if event:
            dlg = EventDialogEx(self.MainWindow, event)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                data = dlg.get_data()
                event.EventName = data['name']
                event.EventDate = data['date']
                event.EventTime = data['time']
                event.Location = data['location']
                event.Description = data['description']
                events.export_json("datasets/events.json")
                QMessageBox.information(self.MainWindow, "Success", "Event updated!")
                self.load_events()
                self.load_event_combo()
                self.load_checkin_event_combo()

    def delete_event(self):
        row = self.eventTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an event to delete!")
            return
        reply = QMessageBox.question(
            self.MainWindow, "Confirm",
            "Are you sure you want to delete this event?\nAll related registrations will be deleted!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event_id = self.eventTable.item(row, 0).text()
            events = Events()
            events.import_json("datasets/events.json")
            events.delete_event(event_id)
            events.export_json("datasets/events.json")
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            regs.list = [r for r in regs.list if r.EventId != event_id]
            regs.export_json("datasets/registrations.json")
            QMessageBox.information(self.MainWindow, "Success", "Event deleted!")
            self.load_events()
            self.load_event_combo()
            self.load_checkin_event_combo()

    def view_event_details(self):
        row = self.eventTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an event!")
            return
        event_id = self.eventTable.item(row, 0).text()
        events = Events()
        events.import_json("datasets/events.json")
        event = events.find_event(event_id)
        if event:
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            total_reg = regs.count_registered_by_event(event_id)
            total_checkin = regs.count_checkedin_by_event(event_id)
            details = (
                f"<h2>{event.EventName}</h2>"
                f"<p><b>📅 Date:</b> {event.EventDate}</p>"
                f"<p><b>🕐 Time:</b> {event.EventTime}</p>"
                f"<p><b>📍 Location:</b> {event.Location}</p>"
                f"<p><b>📝 Description:</b> {event.Description or 'None'}</p>"
                f"<hr><p><b>👥 Total Registered:</b> {total_reg}</p>"
                f"<p><b>✅ Checked-in:</b> {total_checkin}</p>"
            )
            QMessageBox.information(self.MainWindow, "Event Details", details)

    def load_attendees(self):
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        self.attendeeTable.setRowCount(len(attendees.list))
        for row, a in enumerate(attendees.list):
            self.attendeeTable.setItem(row, 0, QTableWidgetItem(a.AttendeeId))
            self.attendeeTable.setItem(row, 1, QTableWidgetItem(a.Name))
            self.attendeeTable.setItem(row, 2, QTableWidgetItem(a.Email))
            self.attendeeTable.setItem(row, 3, QTableWidgetItem(a.Phone or ""))
            self.attendeeTable.setItem(row, 4, QTableWidgetItem(a.Organization or ""))
            self.attendeeTable.setItem(row, 5, QTableWidgetItem(a.Position or ""))

    def search_attendees(self):
        keyword = self.attendeeSearch.text().strip()
        if not keyword:
            self.load_attendees()
            return
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        results = attendees.search_attendees(keyword)
        self.attendeeTable.setRowCount(len(results))
        for row, a in enumerate(results):
            self.attendeeTable.setItem(row, 0, QTableWidgetItem(a.AttendeeId))
            self.attendeeTable.setItem(row, 1, QTableWidgetItem(a.Name))
            self.attendeeTable.setItem(row, 2, QTableWidgetItem(a.Email))
            self.attendeeTable.setItem(row, 3, QTableWidgetItem(a.Phone or ""))
            self.attendeeTable.setItem(row, 4, QTableWidgetItem(a.Organization or ""))
            self.attendeeTable.setItem(row, 5, QTableWidgetItem(a.Position or ""))

    def add_attendee(self):
        dlg = AttendeeDialogEx(self.MainWindow)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            attendees = Attendees()
            attendees.import_json("datasets/attendees.json")
            for a in attendees.list:
                if a.Email.lower() == data['email'].lower():
                    QMessageBox.warning(self.MainWindow, "Error", "Email already exists!")
                    return
            att = Attendee()
            att.AttendeeId = "att_" + str(uuid.uuid4())[:8]
            att.Name = data['name']
            att.Email = data['email']
            att.Phone = data['phone']
            att.Organization = data['organization']
            att.Position = data['position']
            attendees.add_item(att)
            attendees.export_json("datasets/attendees.json")
            QMessageBox.information(self.MainWindow, "Success", "Attendee added!")
            self.load_attendees()

    def edit_attendee(self):
        row = self.attendeeTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an attendee to edit!")
            return
        att_id = self.attendeeTable.item(row, 0).text()
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        att = attendees.find_attendee(att_id)
        if att:
            dlg = AttendeeDialogEx(self.MainWindow, att)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                data = dlg.get_data()
                for a in attendees.list:
                    if a.Email.lower() == data['email'].lower() and a.AttendeeId != att_id:
                        QMessageBox.warning(self.MainWindow, "Error", "Email already exists!")
                        return
                att.Name = data['name']
                att.Email = data['email']
                att.Phone = data['phone']
                att.Organization = data['organization']
                att.Position = data['position']
                attendees.export_json("datasets/attendees.json")
                QMessageBox.information(self.MainWindow, "Success", "Attendee updated!")
                self.load_attendees()

    def delete_attendee(self):
        row = self.attendeeTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an attendee to delete!")
            return
        reply = QMessageBox.question(
            self.MainWindow, "Confirm",
            "Are you sure you want to delete this attendee?\nAll related registrations will be deleted!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            att_id = self.attendeeTable.item(row, 0).text()
            attendees = Attendees()
            attendees.import_json("datasets/attendees.json")
            attendees.delete_attendee(att_id)
            attendees.export_json("datasets/attendees.json")
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            regs.list = [r for r in regs.list if r.AttendeeId != att_id]
            regs.export_json("datasets/registrations.json")
            QMessageBox.information(self.MainWindow, "Success", "Attendee deleted!")
            self.load_attendees()

    def load_event_combo(self):
        self.eventCombo.clear()
        events = Events()
        events.import_json("datasets/events.json")
        for e in events.list:
            self.eventCombo.addItem(f"{e.EventName} - {e.EventDate}", e.EventId)

    def load_registrations(self):
        if self.eventCombo.count() == 0:
            self.registrationTable.setRowCount(0)
            return
        event_id = self.eventCombo.currentData()
        if not event_id:
            return
        regs = Registrations()
        regs.import_json("datasets/registrations.json")
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        items = regs.get_registrations_by_event(event_id)
        self.registrationTable.setRowCount(len(items))
        for row, reg in enumerate(items):
            att = attendees.find_attendee(reg.AttendeeId)
            if att:
                self.registrationTable.setItem(row, 0, QTableWidgetItem(reg.RegistrationId))
                self.registrationTable.setItem(row, 1, QTableWidgetItem(att.Name))
                self.registrationTable.setItem(row, 2, QTableWidgetItem(att.Email))
                self.registrationTable.setItem(row, 3, QTableWidgetItem(att.Organization or ""))
                self.registrationTable.setItem(row, 4, QTableWidgetItem(reg.RegistrationDate))
                self.registrationTable.setItem(row, 5, QTableWidgetItem(reg.Status))

    def register_attendee(self):
        if self.eventCombo.count() == 0:
            QMessageBox.warning(self.MainWindow, "Error", "No events available!")
            return
        event_id = self.eventCombo.currentData()
        dlg = RegistrationDialogEx(self.MainWindow)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            att_id = dlg.get_selected_attendee_id()
            if not att_id:
                return
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            if regs.find_registration_by_event_attendee(event_id, att_id):
                QMessageBox.warning(self.MainWindow, "Error", "This person is already registered for the event!")
                return
            reg = Registration()
            reg.RegistrationId = str(uuid.uuid4())[:8].upper()
            reg.EventId = event_id
            reg.AttendeeId = att_id
            reg.RegistrationDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reg.Status = "Registered"
            regs.add_item(reg)
            regs.export_json("datasets/registrations.json")
            QMessageBox.information(self.MainWindow, "Success",
                                    f"Registered!\nRegistration ID: {reg.RegistrationId}")
            self.load_registrations()

    def cancel_registration(self):
        row = self.registrationTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select a registration to cancel!")
            return
        reply = QMessageBox.question(
            self.MainWindow, "Confirm", "Are you sure you want to cancel this registration?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            reg_id = self.registrationTable.item(row, 0).text()
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            regs.delete_registration(reg_id)
            regs.export_json("datasets/registrations.json")
            QMessageBox.information(self.MainWindow, "Success", "Registration cancelled!")
            self.load_registrations()

    def generate_qr_code(self):
        if not QR_AVAILABLE:
            QMessageBox.warning(self.MainWindow, "Error",
                                "qrcode library not installed!\nInstall: pip install qrcode[pil]")
            return
        row = self.registrationTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select a registration!")
            return
        reg_id = self.registrationTable.item(row, 0).text()
        att_name = self.registrationTable.item(row, 1).text()
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(reg_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        qimage = QImage()
        qimage.loadFromData(buf.read())
        pixmap = QPixmap.fromImage(qimage)
        qr_dlg = QDialog(self.MainWindow)
        qr_dlg.setWindowTitle("Check-in QR Code")
        qr_dlg.resize(400, 450)
        lay = QVBoxLayout()
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_code = QLabel(f"<h3>{att_name}</h3><h2>ID: {reg_id}</h2>")
        lbl_code.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(lbl_img)
        lay.addWidget(lbl_code)
        qr_dlg.setLayout(lay)
        qr_dlg.exec()

    def load_checkin_event_combo(self):
        self.checkinEventCombo.clear()
        events = Events()
        events.import_json("datasets/events.json")
        for e in events.list:
            self.checkinEventCombo.addItem(f"{e.EventName} - {e.EventDate}", e.EventId)

    def load_checkin_stats(self):
        if self.checkinEventCombo.count() == 0:
            self.totalRegisteredLabel.setText("0")
            self.totalCheckedinLabel.setText("0")
            self.checkinTable.setRowCount(0)
            return
        event_id = self.checkinEventCombo.currentData()
        if not event_id:
            return
        regs = Registrations()
        regs.import_json("datasets/registrations.json")
        self.totalRegisteredLabel.setText(str(regs.count_registered_by_event(event_id)))
        self.totalCheckedinLabel.setText(str(regs.count_checkedin_by_event(event_id)))
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        checkedin = [r for r in regs.get_registrations_by_event(event_id)
                     if r.Status == "Checked-in"]
        self.checkinTable.setRowCount(len(checkedin))
        for row, reg in enumerate(checkedin):
            att = attendees.find_attendee(reg.AttendeeId)
            if att:
                self.checkinTable.setItem(row, 0, QTableWidgetItem(att.Name))
                self.checkinTable.setItem(row, 1, QTableWidgetItem(att.Email))
                self.checkinTable.setItem(row, 2, QTableWidgetItem(att.Organization or ""))
                self.checkinTable.setItem(row, 3, QTableWidgetItem(reg.CheckinTime or ""))
                self.checkinTable.setItem(row, 4, QTableWidgetItem(reg.RegistrationId))

    def perform_checkin(self):
        code = self.checkinCode.text().strip().upper()
        if not code:
            QMessageBox.warning(self.MainWindow, "Error", "Please enter registration ID!")
            return
        regs = Registrations()
        regs.import_json("datasets/registrations.json")
        success, message = regs.checkin(code)
        if success:
            regs.export_json("datasets/registrations.json")
            QMessageBox.information(self.MainWindow, "Success", message)
            self.checkinCode.clear()
            self.load_checkin_stats()
        else:
            QMessageBox.warning(self.MainWindow, "Error", message)

    def apply_stylesheet(self):
        self.MainWindow.setStyleSheet("""
            QMainWindow { background-color: #ecf0f1; }
            QPushButton {
                background-color: #3498db; color: white;
                border: none; padding: 8px 15px;
                border-radius: 4px; font-size: 12px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:disabled { background-color: #95a5a6; color: #ecf0f1; }
            QTableWidget { background-color: white;
                           border: 1px solid #bdc3c7; border-radius: 4px; }
            QHeaderView::section { background-color: #34495e; color: white;
                                   padding: 8px; border: none; font-weight: bold; }
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit {
                padding: 6px; border: 1px solid #bdc3c7;
                border-radius: 4px; background-color: white;
            }
            QLineEdit:disabled { background-color: #e0e0e0; color: #7f8c8d; }
            QGroupBox { border: 2px solid #bdc3c7; border-radius: 5px;
                        margin-top: 10px; font-weight: bold; padding: 15px; }
            QGroupBox::title { subcontrol-origin: margin;
                               subcontrol-position: top left;
                               padding: 5px 10px; background-color: white; }
            QTabWidget::pane { border: 1px solid #bdc3c7; border-radius: 4px; }
            QTabBar::tab { background: #ecf0f1; padding: 8px 16px;
                           border-radius: 4px 4px 0 0; font-size: 12px; }
            QTabBar::tab:selected { background: white; color: #2c3e50;
                                    font-weight: bold; }
        """)