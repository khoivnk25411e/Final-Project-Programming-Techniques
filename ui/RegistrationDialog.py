from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_RegistrationDialog(object):
    def setupUi(self, RegistrationDialog):
        RegistrationDialog.setObjectName("RegistrationDialog")
        RegistrationDialog.resize(400, 200)
        RegistrationDialog.setWindowTitle("Đăng Ký Người Tham Dự")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(RegistrationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Form Layout
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        
        # Chọn Người Tham Dự
        self.label = QtWidgets.QLabel("Chọn Người Tham Dự:")
        self.attendeeCombo = QtWidgets.QComboBox()
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.attendeeCombo)
        
        self.verticalLayout.addLayout(self.formLayout)
        
        # Spacer
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        # Buttons
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        
        self.btnRegister = QtWidgets.QPushButton("💾 Đăng Ký")
        self.btnRegister.setStyleSheet("padding: 8px 15px;")
        self.horizontalLayout.addWidget(self.btnRegister)
        
        self.btnCancel = QtWidgets.QPushButton("❌ Hủy")
        self.btnCancel.setStyleSheet("padding: 8px 15px;")
        self.horizontalLayout.addWidget(self.btnCancel)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.btnCancel.clicked.connect(RegistrationDialog.reject)
        
        QtCore.QMetaObject.connectSlotsByName(RegistrationDialog)
