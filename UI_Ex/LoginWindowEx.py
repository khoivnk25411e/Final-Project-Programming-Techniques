import json

from PyQt6.QtWidgets import QLineEdit, QMessageBox, QMainWindow

from ui.LoginWindow import Ui_LoginWindow

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
    def toggle_password_visibility(self):
        if self.lineEditPassword.echoMode() == QLineEdit.EchoMode.Password:
            self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btnTogglePwd.setText("🙈")
        else:
            self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.btnTogglePwd.setText("👁")
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
    def process_login(self):
        username = self.lineEditUsername.text().strip()
        password = self.lineEditPassword.text()

        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return







