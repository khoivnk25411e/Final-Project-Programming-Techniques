from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_AttendeeDialog(object):
    def setupUi(self, AttendeeDialog):
        AttendeeDialog.setObjectName("AttendeeDialog")
        AttendeeDialog.resize(500, 350)
        AttendeeDialog.setWindowTitle("Thêm/Sửa Người Tham Dự")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(AttendeeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Form Layout
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        
        # Họ Tên
        self.label = QtWidgets.QLabel("Họ Tên:")
        self.nameInput = QtWidgets.QLineEdit()
        self.nameInput.setPlaceholderText("Nhập họ tên...")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.nameInput)
        
        # Email
        self.label_2 = QtWidgets.QLabel("Email:")
        self.emailInput = QtWidgets.QLineEdit()
        self.emailInput.setPlaceholderText("Nhập email...")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.emailInput)
        
        # Số Điện Thoại
        self.label_3 = QtWidgets.QLabel("Số Điện Thoại:")
        self.phoneInput = QtWidgets.QLineEdit()
        self.phoneInput.setPlaceholderText("Nhập số điện thoại...")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.phoneInput)
        
        # Tổ Chức
        self.label_4 = QtWidgets.QLabel("Tổ Chức:")
        self.organizationInput = QtWidgets.QLineEdit()
        self.organizationInput.setPlaceholderText("Nhập tổ chức...")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.organizationInput)
        
        # Chức Vụ
        self.label_5 = QtWidgets.QLabel("Chức Vụ:")
        self.positionInput = QtWidgets.QLineEdit()
        self.positionInput.setPlaceholderText("Nhập chức vụ...")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.positionInput)
        
        self.verticalLayout.addLayout(self.formLayout)
        
        # Spacer
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        # Buttons
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        
        self.btnSave = QtWidgets.QPushButton("💾 Lưu")
        self.btnSave.setStyleSheet("padding: 8px 15px;")
        self.horizontalLayout.addWidget(self.btnSave)
        
        self.btnCancel = QtWidgets.QPushButton("❌ Hủy")
        self.btnCancel.setStyleSheet("padding: 8px 15px;")
        self.horizontalLayout.addWidget(self.btnCancel)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.btnCancel.clicked.connect(AttendeeDialog.reject)
        
        QtCore.QMetaObject.connectSlotsByName(AttendeeDialog)
