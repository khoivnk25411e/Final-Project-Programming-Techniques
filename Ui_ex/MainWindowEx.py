from PyQt6.QtWidgets import (QMessageBox, QTableWidgetItem, QHeaderView,
                             QDialog, QVBoxLayout, QLabel, QMainWindow)
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtGui

try:
    from matplotlib import pyplot as plt
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
    import matplotlib
    matplotlib.use("QtAgg")
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
from ui.MainWindow import Ui_MainWindow
from Ui_ex.EventDialogEx import EventDialogEx
from Ui_ex.AttendeeDialogEx import AttendeeDialogEx
from Ui_ex.RegistrationDialogEx import RegistrationDialogEx
from Ui_ex.UserDialogEx import UserDialogEx
from Ui_ex.ChangePasswordDialogEx import ChangePasswordDialogEx
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
                "QLabel{background:#ef4444;color:white;border-radius:5px;"
                "font-size:11px;font-weight:bold;padding:0 8px;}"
            )
        else:
            self.lblRoleBadge.setText("USER")

        idx = self.tabWidget.indexOf(self.userMgmtTab)
        if not is_admin and idx >= 0:
            self.tabWidget.removeTab(idx)

        if not is_admin:
            self.btnAddEvent.setEnabled(False)
            self.btnEditEvent.setEnabled(False)
            self.btnDeleteEvent.setEnabled(False)

            self.btnAddAttendee.setEnabled(False)
            self.btnEditAttendee.setEnabled(False)
            self.btnDeleteAttendee.setEnabled(False)

            self.btnRegisterAttendee.setEnabled(False)
            self.btnCancelRegistration.setEnabled(False)
            self.btnGenerateQR.setEnabled(False)

            self.btnCheckin.setEnabled(False)
            self.btnScanQR.setEnabled(False)
            self.checkinCode.setEnabled(False)
            self.checkinCode.setPlaceholderText("Admin access required for Check-in")

            self.btnRefreshEvent.setEnabled(True)
            self.btnRefreshAttendee.setEnabled(True)
            self.btnRefreshRegistration.setEnabled(True)
            self.btnRefreshCheckin.setEnabled(True)

    def setupSignalAndSlot(self):
        self.btnChangePassword.clicked.connect(self.change_password)
        self.btnLogout.clicked.connect(self.logout)

        self.eventSearch.textChanged.connect(self.search_events)
        self.btnAddEvent.clicked.connect(self.add_event)
        self.btnViewEvent.clicked.connect(self.view_event_details)
        self.btnEditEvent.clicked.connect(self.edit_event)
        self.btnDeleteEvent.clicked.connect(self.delete_event)
        self.btnRefreshEvent.clicked.connect(self.load_events)
        self.btnRefreshEvent.clicked.connect(self.load_events)
        self.btnExportEvent.clicked.connect(self.export_events_csv)
        self.btnPrevEvent.clicked.connect(lambda: self._prev_page("eventTable"))
        self.btnNextEvent.clicked.connect(lambda: self._next_page("eventTable"))

        self.attendeeSearch.textChanged.connect(self.search_attendees)
        self.btnAddAttendee.clicked.connect(self.add_attendee)
        self.btnEditAttendee.clicked.connect(self.edit_attendee)
        self.btnDeleteAttendee.clicked.connect(self.delete_attendee)
        self.btnRefreshAttendee.clicked.connect(self.load_attendees)
        self.btnExportAttendee.clicked.connect(self.export_attendees_csv)
        self.btnPrevAttendee.clicked.connect(lambda: self._prev_page("attendeeTable"))
        self.btnNextAttendee.clicked.connect(lambda: self._next_page("attendeeTable"))

        self.eventCombo.currentIndexChanged.connect(self.load_registrations)
        self.btnRegisterAttendee.clicked.connect(self.register_attendee)
        self.btnGenerateQR.clicked.connect(self.generate_qr_code)
        self.btnCancelRegistration.clicked.connect(self.cancel_registration)
        self.btnRefreshRegistration.clicked.connect(self.load_registrations)
        self.btnExportRegistration.clicked.connect(self.export_registrations_csv)
        self.btnPrevRegistration.clicked.connect(lambda: self._prev_page("registrationTable"))
        self.btnNextRegistration.clicked.connect(lambda: self._next_page("registrationTable"))

        self.checkinEventCombo.currentIndexChanged.connect(self.load_checkin_stats)
        self.btnCheckin.clicked.connect(self.perform_checkin)
        self.btnScanQR.clicked.connect(self.scan_qr_checkin)
        self.btnRefreshCheckin.clicked.connect(self.load_checkin_stats)
        self.btnExportCheckin.clicked.connect(self.export_checkin_csv)

        self.statsEventCombo.currentIndexChanged.connect(self.refresh_chart)
        self.btnStatsBar.clicked.connect(self.show_bar_chart)
        self.btnStatsLine.clicked.connect(self.show_line_chart)
        self.btnStatsPie.clicked.connect(self.show_pie_chart)

        user = getattr(self, 'login_user', None)
        if user and user.Role == "admin":
            self.btnAddUser.clicked.connect(self.add_user)
            self.btnEditUser.clicked.connect(self.edit_user)
            self.btnDeleteUser.clicked.connect(self.delete_user)
            self.btnResetUserPwd.clicked.connect(self.reset_user_password)
            self.btnRefreshUser.clicked.connect(self.load_users)
        else:
            self.btnRefreshEvent.clicked.connect(self.load_events)
            self.btnRefreshAttendee.clicked.connect(self.load_attendees)
            self.btnRefreshRegistration.clicked.connect(self.load_registrations)
            self.btnRefreshCheckin.clicked.connect(self.load_checkin_stats)

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
        self.load_stats_event_combo()

        for tbl in [self.eventTable, self.attendeeTable,
                    self.registrationTable, self.checkinTable, self.userTable]:
            tbl.setAlternatingRowColors(True)
        self.setup_chart()
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
            "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.MainWindow.close()
            from Ui_ex.LoginWindowEx import LoginWindowEx
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
            QMessageBox.information(self.MainWindow, "Success", "New account created successfully!")
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
            QMessageBox.information(self.MainWindow, "Success", "Account updated successfully!")
            self.load_users()

    def delete_user(self):
        row = self.userTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an account to delete!")
            return
        user_id = self.userTable.item(row, 0).text()

        if getattr(self, 'login_user', None) and self.login_user.UserId == user_id:
            QMessageBox.warning(self.MainWindow, "Error", "You cannot delete the currently logged-in account!")
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
            QMessageBox.information(self.MainWindow, "Success", "Account deleted successfully!")
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

    PAGE_SIZE = 10

    def _fill_table(self, table, rows_data):
        table.setRowCount(len(rows_data))
        for row, cols in enumerate(rows_data):
            for col, val in enumerate(cols):
                table.setItem(row, col, QTableWidgetItem(str(val) if val else ""))

    def search_events(self):
        keyword = self.eventSearch.text().strip()
        if not keyword:
            self.load_events()
            return
        events = Events()
        events.import_json("datasets/events.json")
        keyword_lower = keyword.lower()
        results = [
            e for e in events.list
            if keyword_lower in e.EventName.lower()
            or keyword_lower in e.Location.lower()
            or keyword_lower in (e.Description or "").lower()
        ]
        self._setup_pagination(
            self.eventTable, results,
            self._fill_event_table,
            self.lblPageEvent, self.btnPrevEvent, self.btnNextEvent
        )

    def _fill_event_table(self, event_list):
        self.eventTable.setRowCount(len(event_list))
        for row, event in enumerate(event_list):
            self.eventTable.setItem(row, 0, QTableWidgetItem(event.EventId))
            self.eventTable.setItem(row, 1, QTableWidgetItem(event.EventName))
            self.eventTable.setItem(row, 2, QTableWidgetItem(event.EventDate))
            self.eventTable.setItem(row, 3, QTableWidgetItem(event.EventTime))
            self.eventTable.setItem(row, 4, QTableWidgetItem(event.Location))
            self.eventTable.setItem(row, 5, QTableWidgetItem(event.Description or ""))

    def load_events(self):
        events = Events()
        events.import_json("datasets/events.json")
        self._setup_pagination(
            self.eventTable, events.list,
            self._fill_event_table,
            self.lblPageEvent, self.btnPrevEvent, self.btnNextEvent
        )

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
            QMessageBox.information(self.MainWindow, "Success", "New event added successfully!")
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
                QMessageBox.information(self.MainWindow, "Success", "Event updated successfully!")
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
            QMessageBox.information(self.MainWindow, "Success", "Event deleted successfully!")
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
                f"<p><b>📝 Description:</b> {event.Description or 'N/A'}</p>"
                f"<hr><p><b>👥 Total Registered:</b> {total_reg}</p>"
                f"<p><b>✅ Checked-in:</b> {total_checkin}</p>"
            )
            QMessageBox.information(self.MainWindow, "Event Details", details)

    def _fill_attendee_table(self, attendee_list):
        self.attendeeTable.setRowCount(len(attendee_list))
        for row, a in enumerate(attendee_list):
            self.attendeeTable.setItem(row, 0, QTableWidgetItem(a.AttendeeId))
            self.attendeeTable.setItem(row, 1, QTableWidgetItem(a.Name))
            self.attendeeTable.setItem(row, 2, QTableWidgetItem(a.Email))
            self.attendeeTable.setItem(row, 3, QTableWidgetItem(a.Phone or ""))
            self.attendeeTable.setItem(row, 4, QTableWidgetItem(a.Organization or ""))
            self.attendeeTable.setItem(row, 5, QTableWidgetItem(a.Position or ""))

    def load_attendees(self):
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        self._setup_pagination(
            self.attendeeTable, attendees.list,
            self._fill_attendee_table,
            self.lblPageAttendee, self.btnPrevAttendee, self.btnNextAttendee
        )

    def search_attendees(self):
        keyword = self.attendeeSearch.text().strip()
        if not keyword:
            self.load_attendees()
            return
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")
        results = attendees.search_attendees(keyword)
        self._setup_pagination(
            self.attendeeTable, results,
            self._fill_attendee_table,
            self.lblPageAttendee, self.btnPrevAttendee, self.btnNextAttendee
        )

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
            QMessageBox.information(self.MainWindow, "Success", "Attendee added successfully!")
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
                QMessageBox.information(self.MainWindow, "Success", "Attendee updated successfully!")
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
            QMessageBox.information(self.MainWindow, "Success", "Attendee deleted successfully!")
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
        self._reg_attendee_map = {}
        for reg in items:
            att = attendees.find_attendee(reg.AttendeeId)
            if att:
                self._reg_attendee_map[reg.RegistrationId] = (reg, att)

        valid_items = [reg for reg in items if reg.RegistrationId in self._reg_attendee_map]
        self._setup_pagination(
            self.registrationTable, valid_items,
            self._fill_registration_table,
            self.lblPageRegistration, self.btnPrevRegistration, self.btnNextRegistration
        )

    def _fill_registration_table(self, reg_list):
        self.registrationTable.setRowCount(len(reg_list))
        for row, reg in enumerate(reg_list):
            pair = self._reg_attendee_map.get(reg.RegistrationId)
            if not pair:
                continue
            reg, att = pair
            is_checkedin = reg.Status == "Checked-in"
            values = [
                reg.RegistrationId, att.Name, att.Email,
                att.Organization or "", reg.RegistrationDate,
                "✅ " + reg.Status if is_checkedin else reg.Status,
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                if is_checkedin:
                    item.setBackground(QtGui.QColor("#F9E79F"))
                    item.setForeground(QtGui.QColor("#7D6608"))
                self.registrationTable.setItem(row, col, item)
        pass

    def register_attendee(self):
        if self.eventCombo.count() == 0:
            QMessageBox.warning(self.MainWindow, "Error", "No events available!")
            return
        event_id = self.eventCombo.currentData()
        dlg = RegistrationDialogEx(self.MainWindow, event_id=event_id)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            att_ids = dlg.get_selected_attendee_ids()
            if not att_ids:
                return

            regs = Registrations()
            regs.import_json("datasets/registrations.json")

            success_list = []
            skip_list    = []

            for att_id in att_ids:
                if regs.find_registration_by_event_attendee(event_id, att_id):
                    skip_list.append(att_id)
                    continue
                reg = Registration()
                reg.RegistrationId   = str(uuid.uuid4())[:8].upper()
                reg.EventId          = event_id
                reg.AttendeeId       = att_id
                reg.RegistrationDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                reg.Status           = "Registered"
                regs.add_item(reg)
                success_list.append(reg.RegistrationId)

            if success_list:
                regs.export_json("datasets/registrations.json")

            msg = ""
            if success_list:
                codes = ", ".join(success_list)
                msg += f"✅ Registered {len(success_list)} attendee(s)!\nCodes: {codes}"
            if skip_list:
                msg += f"\n⚠️ {len(skip_list)} attendee(s) already registered (skipped)."

            if msg:
                QMessageBox.information(self.MainWindow, "Registration Result", msg)

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
            QMessageBox.information(self.MainWindow, "Success", "Registration canceled successfully!")
            self.load_registrations()

    def generate_qr_code(self):
        if not QR_AVAILABLE:
            QMessageBox.warning(self.MainWindow, "Error",
                                "qrcode library not installed!\nInstall with: pip install qrcode[pil]")
            return
        row = self.registrationTable.currentRow()
        if row < 0:
            QMessageBox.warning(self.MainWindow, "Error", "Please select a registration!")
            return
        reg_id    = self.registrationTable.item(row, 0).text()
        att_name  = self.registrationTable.item(row, 1).text()
        att_email = self.registrationTable.item(row, 2).text()
        att_org   = self.registrationTable.item(row, 3).text()

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(reg_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        qimage = QImage()
        qimage.loadFromData(buf.read())
        pixmap = QPixmap.fromImage(qimage)

        from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFileDialog, QApplication

        qr_dlg = QDialog(self.MainWindow)
        qr_dlg.setWindowTitle("Check-in QR Code")
        qr_dlg.setMinimumWidth(420)
        qr_dlg.setStyleSheet("background-color: #f4f6f7;")

        lay = QVBoxLayout()
        lay.setSpacing(10)
        lay.setContentsMargins(20, 20, 20, 20)

        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(lbl_img)

        info_text = (
            f"<div style='text-align:center;'>"
            f"<h3 style='margin:0;color:#3b82f6;'>{att_name}</h3>"
            f"<p style='margin:2px;color:#7f8c8d;font-size:12px;'>{att_email}</p>"
            f"<p style='margin:2px;color:#7f8c8d;font-size:12px;'>{att_org}</p>"
            f"<h2 style='color:#2980b9;margin-top:6px;'>🎫 Code: {reg_id}</h2>"
            f"</div>"
        )
        lbl_info = QLabel(info_text)
        lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_info.setTextFormat(Qt.TextFormat.RichText)
        lay.addWidget(lbl_info)

        btn_layout = QHBoxLayout()

        btn_save = QPushButton("💾 Save QR Image")
        btn_save.setStyleSheet(
            "QPushButton { background:#3b82f6; color:white; border-radius:6px;"
            "font-size:13px; font-weight:bold; padding:8px 16px; }"
            "QPushButton:hover { background:#1e293b; }"
        )
        btn_copy = QPushButton("📋 Copy Code")
        btn_copy.setStyleSheet(
            "QPushButton { background:#2563eb; color:white; border-radius:6px;"
            "font-size:13px; font-weight:bold; padding:8px 16px; }"
            "QPushButton:hover { background:#2563eb; }"
        )
        btn_close = QPushButton("✖ Close")
        btn_close.setStyleSheet(
            "QPushButton { background:#ef4444; color:white; border-radius:6px;"
            "font-size:13px; padding:8px 16px; }"
            "QPushButton:hover { background:#dc2626; }"
        )

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_copy)
        btn_layout.addWidget(btn_close)
        lay.addLayout(btn_layout)
        qr_dlg.setLayout(lay)

        def save_qr():
            default_name = f"QR_{att_name.replace(' ', '_')}_{reg_id}.png"
            file_path, _ = QFileDialog.getSaveFileName(
                qr_dlg, "Save QR Code", default_name,
                "PNG Image (*.png);;All Files (*)"
            )
            if file_path:
                buf2 = BytesIO()
                img.save(buf2, format="PNG")
                buf2.seek(0)
                with open(file_path, "wb") as f:
                    f.write(buf2.read())
                QMessageBox.information(qr_dlg, "Saved", f"QR Code saved!\n📁 {file_path}")

        def copy_code():
            QApplication.clipboard().setText(reg_id)
            QMessageBox.information(qr_dlg, "Copied", f"Code copied to clipboard!\n🎫 {reg_id}")

        btn_save.clicked.connect(save_qr)
        btn_copy.clicked.connect(copy_code)
        btn_close.clicked.connect(qr_dlg.accept)

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
                     if r.Status == "Checked-in" or r.Status == "Đã check-in"]
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
            QMessageBox.warning(self.MainWindow, "Error", "Please enter a registration code!")
            return

        event_id = self.checkinEventCombo.currentData()
        if not event_id:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an event first!")
            return

        regs = Registrations()
        regs.import_json("datasets/registrations.json")
        success, message = regs.checkin_for_event(code, event_id)
        if success:
            regs.export_json("datasets/registrations.json")
            QMessageBox.information(self.MainWindow, "Success", message)
            self.checkinCode.clear()
            self.load_checkin_stats()
        else:
            QMessageBox.warning(self.MainWindow, "Error", message)

    def scan_qr_checkin(self):
        from Ui_ex.QRScannerDialogEx import QRScannerDialogEx

        event_id = self.checkinEventCombo.currentData()
        if not event_id:
            QMessageBox.warning(self.MainWindow, "Error", "Please select an event first!")
            return

        def checkin_callback(qr_code):
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            success, message = regs.checkin_for_event(qr_code.upper(), event_id)
            if success:
                regs.export_json("datasets/registrations.json")
                QTimer.singleShot(500, self.load_checkin_stats)
            return success, message

        scanner = QRScannerDialogEx(self.MainWindow, callback=checkin_callback)
        scanner.exec()

    def _get_file_path(self, default_filename):
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self.MainWindow, "Export to CSV", default_filename,
            "CSV Files (*.csv);;All Files (*)"
        )
        return file_path

    def _write_csv(self, file_path, headers, rows):
        import csv
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def export_events_csv(self):
        file_path = self._get_file_path("events.csv")
        if not file_path:
            return
        try:
            events = Events()
            events.import_json("datasets/events.json")
            headers = ["ID", "Event Name", "Date", "Time", "Venue", "Description"]
            rows = [
                [e.EventId, e.EventName, e.EventDate, e.EventTime,
                 e.Location, e.Description or ""]
                for e in events.list
            ]
            self._write_csv(file_path, headers, rows)
            QMessageBox.information(self.MainWindow, "Exported",
                f"✅ Exported {len(rows)} events!\n📁 {file_path}")
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Error", f"Export failed:\n{str(e)}")

    def export_attendees_csv(self):
        file_path = self._get_file_path("attendees.csv")
        if not file_path:
            return
        try:
            attendees = Attendees()
            attendees.import_json("datasets/attendees.json")
            headers = ["ID", "Full Name", "Email", "Phone", "Organization", "Position"]
            rows = [
                [a.AttendeeId, a.Name, a.Email, a.Phone or "",
                 a.Organization or "", a.Position or ""]
                for a in attendees.list
            ]
            self._write_csv(file_path, headers, rows)
            QMessageBox.information(self.MainWindow, "Exported",
                f"✅ Exported {len(rows)} attendees!\n📁 {file_path}")
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Error", f"Export failed:\n{str(e)}")

    def export_registrations_csv(self):
        file_path = self._get_file_path("registrations.csv")
        if not file_path:
            return
        try:
            event_id = self.eventCombo.currentData()
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            attendees = Attendees()
            attendees.import_json("datasets/attendees.json")
            items = regs.get_registrations_by_event(event_id) if event_id else regs.list
            headers = ["Reg. ID", "Full Name", "Email", "Organization", "Reg. Date", "Status"]
            rows = []
            for reg in items:
                att = attendees.find_attendee(reg.AttendeeId)
                rows.append([
                    reg.RegistrationId,
                    att.Name if att else "",
                    att.Email if att else "",
                    att.Organization or "" if att else "",
                    reg.RegistrationDate,
                    reg.Status,
                ])
            self._write_csv(file_path, headers, rows)
            QMessageBox.information(self.MainWindow, "Exported",
                f"✅ Exported {len(rows)} registrations!\n📁 {file_path}")
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Error", f"Export failed:\n{str(e)}")

    def export_checkin_csv(self):
        file_path = self._get_file_path("checkin_list.csv")
        if not file_path:
            return
        try:
            event_id = self.checkinEventCombo.currentData()
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            attendees = Attendees()
            attendees.import_json("datasets/attendees.json")
            items = [
                r for r in (regs.get_registrations_by_event(event_id) if event_id else regs.list)
                if r.Status == "Checked-in"
            ]
            headers = ["Full Name", "Email", "Organization", "Check-in Time", "Reg. Code"]
            rows = []
            for reg in items:
                att = attendees.find_attendee(reg.AttendeeId)
                rows.append([
                    att.Name if att else "",
                    att.Email if att else "",
                    att.Organization or "" if att else "",
                    reg.CheckinTime if hasattr(reg, "CheckinTime") else "",
                    reg.RegistrationId,
                ])
            self._write_csv(file_path, headers, rows)
            QMessageBox.information(self.MainWindow, "Exported",
                f"✅ Exported {len(rows)} check-ins!\n📁 {file_path}")
        except Exception as e:
            QMessageBox.warning(self.MainWindow, "Error", f"Export failed:\n{str(e)}")

    def _setup_pagination(self, table, data_list, fill_func, page_label, prev_btn, next_btn):
        if not hasattr(self, '_pages'):
            self._pages = {}

        name = table.objectName()
        self._pages[name] = {
            'data': data_list,
            'page': 0,
            'fill_func': fill_func,
            'label': page_label,
            'prev': prev_btn,
            'next': next_btn,
        }
        self._render_page(name)

    def _render_page(self, name):
        state = self._pages[name]
        data     = state['data']
        page     = state['page']
        total    = max(1, (len(data) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        start    = page * self.PAGE_SIZE
        end      = start + self.PAGE_SIZE
        chunk    = data[start:end]

        state['fill_func'](chunk)
        state['label'].setText(f"Page {page + 1} / {total}")
        state['prev'].setEnabled(page > 0)
        state['next'].setEnabled(page < total - 1)

    def _prev_page(self, name):
        if self._pages[name]['page'] > 0:
            self._pages[name]['page'] -= 1
            self._render_page(name)

    def _next_page(self, name):
        state = self._pages[name]
        total = max(1, (len(state['data']) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        if state['page'] < total - 1:
            state['page'] += 1
            self._render_page(name)

    def setup_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            lbl = QLabel("⚠️ matplotlib not installed!\npip install matplotlib")
            lbl.setStyleSheet("color: red; font-size: 13px; padding: 20px;")
            self.verticalLayoutStatsPlot.addWidget(lbl)
            return

        self.stats_figure, self.stats_ax = plt.subplots()
        self.stats_figure.patch.set_facecolor("white")
        self.stats_canvas = FigureCanvas(self.stats_figure)

        self.verticalLayoutStatsPlot.addWidget(self.stats_canvas)

        self.show_bar_chart()

    def _set_active_btn(self, active_btn):
        for btn in [self.btnStatsBar, self.btnStatsLine, self.btnStatsPie]:
            if btn is active_btn:
                btn.setStyleSheet(btn.property("active_style"))
            else:
                btn.setStyleSheet(btn.property("inactive_style"))

    def load_stats_event_combo(self):
        self.statsEventCombo.clear()
        self.statsEventCombo.addItem("🌐 All Events", None)
        events = Events()
        events.import_json("datasets/events.json")
        for e in events.list:
            self.statsEventCombo.addItem(f"{e.EventName} - {e.EventDate}", e.EventId)

    def _get_stats_data(self):
        event_id = self.statsEventCombo.currentData()
        events = Events()
        events.import_json("datasets/events.json")
        regs = Registrations()
        regs.import_json("datasets/registrations.json")

        data = {}
        target_events = events.list if event_id is None else [
            e for e in events.list if e.EventId == event_id
        ]

        for e in target_events:
            event_regs = regs.get_registrations_by_event(e.EventId)
            registered = len(event_regs)
            checkedin  = sum(1 for r in event_regs if r.Status == "Checked-in")
            label = e.EventName if len(e.EventName) <= 18 else e.EventName[:15] + "..."
            data[label] = {"registered": registered, "checkedin": checkedin}

        return data

    def refresh_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            return
        if not hasattr(self, 'stats_ax') or not hasattr(self, 'stats_canvas'):
            return
        title = self.stats_ax.get_title()
        if "Line" in title:
            self.show_line_chart()
        elif "Pie" in title:
            self.show_pie_chart()
        else:
            self.show_bar_chart()

    def show_bar_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            return
        if hasattr(self, 'btnStatsBar'):
            self._set_active_btn(self.btnStatsBar)
        data = self._get_stats_data()
        if not data:
            return

        self.stats_figure.clear()
        ax = self.stats_figure.add_subplot(111)
        self.stats_ax = ax

        labels     = list(data.keys())
        registered = [data[k]["registered"] for k in labels]
        checkedin  = [data[k]["checkedin"]  for k in labels]

        x     = range(len(labels))
        width = 0.35

        bars1 = ax.bar([i - width/2 for i in x], registered, width,
                       label="Registered", color="#3498db", alpha=0.85)
        bars2 = ax.bar([i + width/2 for i in x], checkedin, width,
                       label="Checked-in", color="#27ae60", alpha=0.85)

        for bar in bars1:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)
        for bar in bars2:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(int(bar.get_height())), ha='center', va='bottom', fontsize=9)

        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, rotation=15, ha='right', fontsize=9)
        ax.set_ylabel("Number of People")
        ax.set_title("Registration vs Check-in by Event", fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(axis='y', alpha=0.4)
        ax.set_facecolor("#f9f9f9")
        self.stats_figure.tight_layout()
        self.stats_canvas.draw()

    def show_line_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            return
        if hasattr(self, 'btnStatsLine'):
            self._set_active_btn(self.btnStatsLine)

        regs = Registrations()
        regs.import_json("datasets/registrations.json")
        event_id = self.statsEventCombo.currentData()

        items = regs.get_registrations_by_event(event_id) if event_id else regs.list

        if not items:
            QMessageBox.information(self.MainWindow, "Info", "No registration data!")
            return

        from collections import Counter
        date_counts = Counter()
        for r in items:
            date_counts[r.RegistrationDate] += 1

        dates  = sorted(date_counts.keys())
        counts = [date_counts[d] for d in dates]

        cumulative = []
        total = 0
        for c in counts:
            total += c
            cumulative.append(total)

        self.stats_figure.clear()
        ax = self.stats_figure.add_subplot(111)
        self.stats_ax = ax

        ax.plot(dates, cumulative, marker='o', color='#e67e22',
                linewidth=2, markersize=7, label="Cumulative Registrations")
        ax.fill_between(range(len(dates)), cumulative, alpha=0.15, color='#e67e22')

        for i, val in enumerate(cumulative):
            ax.annotate(str(val), (dates[i], val),
                        textcoords="offset points", xytext=(0, 8),
                        ha='center', fontsize=9)

        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=15, ha='right', fontsize=9)
        ax.set_ylabel("Cumulative Registrations")
        ax.set_title("Line Chart: Registration Trend", fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.4)
        ax.set_facecolor("#f9f9f9")
        self.stats_figure.tight_layout()
        self.stats_canvas.draw()

    def show_pie_chart(self):
        if not MATPLOTLIB_AVAILABLE:
            return
        if hasattr(self, 'btnStatsPie'):
            self._set_active_btn(self.btnStatsPie)

        regs = Registrations()
        regs.import_json("datasets/registrations.json")
        event_id = self.statsEventCombo.currentData()

        items = regs.get_registrations_by_event(event_id) if event_id else regs.list

        checkedin     = sum(1 for r in items if r.Status == "Checked-in")
        not_checkedin = len(items) - checkedin

        if checkedin + not_checkedin == 0:
            QMessageBox.information(self.MainWindow, "Info", "No registration data!")
            return

        self.stats_figure.clear()
        ax = self.stats_figure.add_subplot(111)
        self.stats_ax = ax

        sizes  = [checkedin, not_checkedin]
        labels = [f"Checked-in ({checkedin})", f"Not Checked-in ({not_checkedin})"]
        colors = ["#27ae60", "#e74c3c"]
        explode = (0.05, 0)

        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', explode=explode,
            startangle=90, textprops={'fontsize': 10}
        )
        for at in autotexts:
            at.set_fontweight('bold')

        ax.set_title("Pie Chart: Check-in Rate", fontsize=12, fontweight='bold')
        ax.legend(wedges, labels, loc="lower right", fontsize=9)
        self.stats_figure.tight_layout()
        self.stats_canvas.draw()

    def apply_stylesheet(self):
        self.MainWindow.setStyleSheet("""
            QMainWindow { background-color: white; }

            QPushButton {
                background-color: #3b82f6; color: white;
                border: none; padding: 8px 15px;
                border-radius: 5px; font-size: 12px;
            }
            QPushButton:hover   { background-color: #2563eb; }
            QPushButton:pressed { background-color: #1d4ed8; }
            QPushButton:disabled { background-color: #cbd5e1; color: #94a3b8; }

            QTableWidget {
                background-color: white;
                alternate-background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                gridline-color: #e2e8f0;
            }
            QTableWidget::item {
                color: #111827;
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                color: #374151;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: bold;
                font-size: 12px;
            }

            QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit {
                padding: 6px;
                border: 1px solid #d1d5db;
                border-radius: 5px;
                background-color: white;
                color: #111827;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3b82f6;
            }
            QLineEdit:disabled { background-color: #f9fafb; color: #9ca3af; }

            QGroupBox {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
                padding: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 4px 10px;
                background-color: #f1f5f9;
                color: #374151;
                border-radius: 4px;
            }

            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                background: white;
            }
            QTabBar::tab {
                background: #f3f4f6;
                color: #6b7280;
                padding: 8px 16px;
                border-radius: 5px 5px 0 0;
                font-size: 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #111827;
                font-weight: bold;
                border-top: 2px solid #3b82f6;
            }
            QTabBar::tab:hover:!selected {
                background: #e5e7eb;
                color: #374151;
            }

            QScrollBar:vertical {
                background: #f9fafb; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db; border-radius: 4px; min-height: 20px;
            }
            QScrollBar:horizontal {
                background: #f9fafb; height: 8px; border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: #d1d5db; border-radius: 4px; min-width: 20px;
            }

            QLabel { color: #111827; }
            QCheckBox { color: #111827; }
            QWidget#contentWidget { background-color: #f9fafb; }
        """)