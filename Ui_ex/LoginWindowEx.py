import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QLineEdit

from ui.LoginWindow import Ui_LoginWindow
from Ui_ex.ForgotPasswordDialogEx import ForgotPasswordDialogEx
from Ui_ex.ChangePasswordDialogEx import ChangePasswordDialogEx
from models.users import Users

REMEMBER_FILE = "datasets/remember.json"

class LoginWindowEx(Ui_LoginWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.load_remember()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.btnLogin.clicked.connect(self.process_login)
        self.btnExit.clicked.connect(self.MainWindow.close)
        self.btnForgotPassword.clicked.connect(self.process_forgot_password)
        self.btnTogglePwd.clicked.connect(self.toggle_password_visibility)
        self.lineEditPassword.returnPressed.connect(self.process_login)
        self.lineEditUsername.returnPressed.connect(self.lineEditPassword.setFocus)

    # ── Toggle hiện/ẩn mật khẩu ─────────────────────────────────────
    def toggle_password_visibility(self):
        if self.lineEditPassword.echoMode() == QLineEdit.EchoMode.Password:
            self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btnTogglePwd.setText("🙈")
        else:
            self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.btnTogglePwd.setText("👁")

    # ── Ghi nhớ đăng nhập ───────────────────────────────────────────
    def load_remember(self):
        try:
            with open(REMEMBER_FILE, encoding='utf-8') as f:
                data = json.load(f)
                if data.get('remember'):
                    self.lineEditUsername.setText(data.get('username', ''))
                    self.lineEditPassword.setText(data.get('password', ''))
                    self.checkBoxRemember.setChecked(True)
        except FileNotFoundError:
            pass

    def save_remember(self, username, password, remember):
        data = {'remember': remember, 'username': username, 'password': password}
        with open(REMEMBER_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ── Đăng nhập ───────────────────────────────────────────────────
    def process_login(self):
        username = self.lineEditUsername.text().strip()
        password = self.lineEditPassword.text()

        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return

        users = Users()
        users.import_json("datasets/users.json")
        user = users.login(username, password)

        if user is None:
            QMessageBox.warning(self.MainWindow, "Đăng Nhập Thất Bại",
                                "Tên đăng nhập hoặc mật khẩu không đúng!")
            self.lineEditPassword.clear()
            self.lineEditPassword.setFocus()
            return

        # Lưu / xoá remember
        self.save_remember(username, password, self.checkBoxRemember.isChecked())

        # Đóng cửa sổ login
        self.MainWindow.close()

        # Mở cửa sổ chính với thông tin user đăng nhập
        self._open_main_window(user)

    def _open_main_window(self, user):
        from Ui_ex.MainWindowEx import MainWindowEx
        self.main_gui = MainWindowEx()
        self.main_gui.login_user = user          # truyền thông tin user sang MainWindow
        self.main_gui.setupUi(QMainWindow())
        self.main_gui.showWindow()

    # ── Quên mật khẩu ───────────────────────────────────────────────
    def process_forgot_password(self):
        from PyQt6.QtWidgets import QDialog
        dialog = ForgotPasswordDialogEx(self.MainWindow)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user = dialog.get_user()
            if user:
                # Mở dialog đổi mật khẩu, bỏ qua mật khẩu cũ
                change_dlg = ChangePasswordDialogEx(
                    self.MainWindow,
                    current_user=user,
                    skip_old_password=True
                )
                change_dlg.exec()
