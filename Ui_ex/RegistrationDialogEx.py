from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QWidget, QCheckBox,
    QLineEdit, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from models.attendees import Attendees
from models.registrations import Registrations


class RegistrationDialogEx:
    def __init__(self, parent=None, event_id=None):
        self.event_id = event_id
        self._checkboxes = []       # list of (QCheckBox, AttendeeId)
        self._all_available = []    # list of attendee objects

        self.dialog = QDialog(parent)
        self.dialog.setWindowTitle("Register Attendees")
        self.dialog.setMinimumSize(520, 520)
        self.dialog.setStyleSheet("background-color: #f4f6f7;")

        self._build_ui()
        self._load_attendees()

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self.dialog)
        root.setSpacing(10)
        root.setContentsMargins(16, 16, 16, 16)

        # Title
        lbl_title = QLabel("Select Attendees to Register")
        lbl_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #1e293b;")
        root.addWidget(lbl_title)

        # Search bar
        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText("Search by name or email...")
        self.searchBox.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
                background: white;
                color: #1e293b;
            }
        """)
        self.searchBox.textChanged.connect(self._filter_list)
        root.addWidget(self.searchBox)

        # Select All / Deselect All row
        ctrl_row = QHBoxLayout()
        self.btnSelectAll = QPushButton("☑ Select All")
        self.btnSelectAll.setStyleSheet("""
            QPushButton {
                background: #3b82f6; color: white;
                border: none; border-radius: 4px;
                padding: 6px 14px; font-size: 12px;
            }
            QPushButton:hover { background: #2563eb; }
        """)
        self.btnDeselectAll = QPushButton("☐ Deselect All")
        self.btnDeselectAll.setStyleSheet("""
            QPushButton {
                background: #64748b; color: white;
                border: none; border-radius: 4px;
                padding: 6px 14px; font-size: 12px;
            }
            QPushButton:hover { background: #475569; }
        """)
        self.lblCount = QLabel("0 selected")
        self.lblCount.setStyleSheet("color: #64748b; font-size: 12px;")

        ctrl_row.addWidget(self.btnSelectAll)
        ctrl_row.addWidget(self.btnDeselectAll)
        ctrl_row.addStretch()
        ctrl_row.addWidget(self.lblCount)
        root.addLayout(ctrl_row)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #dfe6e9;")
        root.addWidget(line)

        # Scrollable checkbox list
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("""
            QScrollArea { border: 1px solid #e2e8f0; border-radius: 4px; background: white; }
        """)
        self.listWidget = QWidget()
        self.listWidget.setStyleSheet("background: white;")
        self.listLayout = QVBoxLayout(self.listWidget)
        self.listLayout.setSpacing(2)
        self.listLayout.setContentsMargins(8, 8, 8, 8)
        self.listLayout.addStretch()
        self.scrollArea.setWidget(self.listWidget)
        root.addWidget(self.scrollArea)

        # Bottom buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btnRegister = QPushButton("✔ Register Selected")
        self.btnRegister.setStyleSheet("""
            QPushButton {
                background: #3b82f6; color: white;
                border: none; border-radius: 5px;
                padding: 9px 22px; font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background: #2563eb; }
            QPushButton:disabled { background: #95a5a6; }
        """)
        self.btnCancel = QPushButton("✖ Cancel")
        self.btnCancel.setStyleSheet("""
            QPushButton {
                background: #64748b; color: white;
                border: none; border-radius: 5px;
                padding: 9px 22px; font-size: 13px;
            }
            QPushButton:hover { background: #777777; }
        """)
        btn_row.addWidget(self.btnRegister)
        btn_row.addWidget(self.btnCancel)
        root.addLayout(btn_row)

        # Signals
        self.btnSelectAll.clicked.connect(self._select_all)
        self.btnDeselectAll.clicked.connect(self._deselect_all)
        self.btnRegister.clicked.connect(self._validate_and_accept)
        self.btnCancel.clicked.connect(self.dialog.reject)

    # ── Load attendees ────────────────────────────────────────────────────────
    def _load_attendees(self):
        attendees = Attendees()
        attendees.import_json("datasets/attendees.json")

        registered_ids = set()
        if self.event_id:
            regs = Registrations()
            regs.import_json("datasets/registrations.json")
            for reg in regs.get_registrations_by_event(self.event_id):
                registered_ids.add(reg.AttendeeId)

        self._all_available = [
            a for a in attendees.list if a.AttendeeId not in registered_ids
        ]

        self._render_list(self._all_available)

        if not self._all_available:
            self.btnRegister.setEnabled(False)
            self.btnSelectAll.setEnabled(False)
            lbl = QLabel("⚠️ All attendees have already registered for this event.")
            lbl.setStyleSheet("color: #64748b; padding: 10px;")
            self.listLayout.insertWidget(0, lbl)

    def _render_list(self, attendee_list):
        """Xóa list cũ và render lại danh sách checkbox"""
        # Xóa tất cả widget cũ (trừ stretch cuối)
        while self.listLayout.count() > 1:
            item = self.listLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._checkboxes.clear()

        for att in attendee_list:
            cb = QCheckBox(f"  {att.Name}   |   {att.Email}")
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 13px; color: #1e293b;
                    padding: 5px 4px;
                }
                QCheckBox:hover { background-color: #f1f5f9; border-radius: 4px; }
                QCheckBox::indicator { width: 16px; height: 16px; }
            """)
            cb.stateChanged.connect(self._update_count)
            self.listLayout.insertWidget(self.listLayout.count() - 1, cb)
            self._checkboxes.append((cb, att.AttendeeId))

        self._update_count()

    # ── Controls ──────────────────────────────────────────────────────────────
    def _filter_list(self, keyword):
        keyword = keyword.strip().lower()
        if not keyword:
            self._render_list(self._all_available)
            return
        filtered = [
            a for a in self._all_available
            if keyword in a.Name.lower() or keyword in a.Email.lower()
        ]
        self._render_list(filtered)

    def _select_all(self):
        for cb, _ in self._checkboxes:
            cb.setChecked(True)

    def _deselect_all(self):
        for cb, _ in self._checkboxes:
            cb.setChecked(False)

    def _update_count(self):
        count = sum(1 for cb, _ in self._checkboxes if cb.isChecked())
        self.lblCount.setText(f"{count} selected")
        self.btnRegister.setEnabled(count > 0)

    def _validate_and_accept(self):
        selected = self.get_selected_attendee_ids()
        if not selected:
            QMessageBox.warning(self.dialog, "Error", "Please select at least one attendee!")
            return
        self.dialog.accept()

    # ── Public API ────────────────────────────────────────────────────────────
    def get_selected_attendee_ids(self):
        """Trả về list các AttendeeId được chọn"""
        return [att_id for cb, att_id in self._checkboxes if cb.isChecked()]

    def exec(self):
        return self.dialog.exec()