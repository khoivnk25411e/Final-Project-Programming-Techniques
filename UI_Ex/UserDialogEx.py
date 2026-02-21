from PyQt6.QtWidgets import QDialog, QMessageBox
from Event_Check_in_Management.ui.UserDialog import Ui_UserDialog

class UserDialogEx(Ui_UserDialog):
    def __init__(self, parent=None, user_data=None):
        """user_data: đối tượng User nếu đang sửa, None nếu thêm mới"""
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.user_data = user_data
        self.setupSignalAndSlot()
        if user_data:
            self.load_user_data()

    def setupSignalAndSlot(self):
        self.btnSave.clicked.connect(self.validate_and_accept)

    def load_user_data(self):
        self.lineEditFullName.setText(self.user_data.FullName)
        self.lineEditUsername.setText(self.user_data.UserName)
        self.lineEditEmail.setText(self.user_data.Email)
        # Mật khẩu để trống (giữ nguyên nếu không nhập)
        self.lineEditSecQuestion.setText(self.user_data.SecurityQuestion or "")
        self.lineEditSecAnswer.setText(self.user_data.SecurityAnswer or "")
        # Set role
        idx = self.comboRole.findData(self.user_data.Role)
        if idx >= 0:
            self.comboRole.setCurrentIndex(idx)
        # Không cho đổi role của chính mình nếu cần (được xử lý ở Ex)

    def validate_and_accept(self):
        full_name = self.lineEditFullName.text().strip()
        username  = self.lineEditUsername.text().strip()
        email     = self.lineEditEmail.text().strip()
        password  = self.lineEditPassword.text()

        if not full_name or not username or not email:
            QMessageBox.warning(self.dialog, "Lỗi", "Vui lòng điền đầy đủ họ tên, tên đăng nhập và email!")
            return
        if not self.user_data and len(password) < 6:
            QMessageBox.warning(self.dialog, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        if self.user_data and password and len(password) < 6:
            QMessageBox.warning(self.dialog, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        self.dialog.accept()

    def get_data(self):
        return {
            'full_name':       self.lineEditFullName.text().strip(),
            'username':        self.lineEditUsername.text().strip(),
            'email':           self.lineEditEmail.text().strip(),
            'password':        self.lineEditPassword.text(),   # rỗng = giữ nguyên
            'role':            self.comboRole.currentData(),
            'sec_question':    self.lineEditSecQuestion.text().strip(),
            'sec_answer':      self.lineEditSecAnswer.text().strip().lower()
        }

    def exec(self):
        return self.dialog.exec()
