from PyQt6.QtWidgets import QDialog, QCheckBox, QLabel, QMessageBox
from PyQt6.QtCore import Qt

from ui.RegistrationDialog import Ui_RegistrationDialog
from models.attendees import Attendees
from models.registrations import Registrations


class RegistrationDialogEx(QDialog, Ui_RegistrationDialog):

    def __init__(self, parent=None, event_id=None):
        super().__init__(parent)
        self.setupUi(self)

        self.event_id = event_id
        self._checkboxes = []
        self._all_available = []

        self._load_attendees()
        self._connect_signals()

    def _connect_signals(self):
        self.searchBox.textChanged.connect(self._filter_list)
        self.btnSelectAll.clicked.connect(self._select_all)
        self.btnDeselectAll.clicked.connect(self._deselect_all)
        self.btnRegister.clicked.connect(self._validate_and_accept)

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
        while self.listLayout.count() > 1:
            item = self.listLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._checkboxes.clear()

        for att in attendee_list:
            cb = QCheckBox(f"  {att.Name}   |   {att.Email}")
            cb.setStyleSheet(
                "QCheckBox { font-size: 13px; color: #1e293b; padding: 5px 4px; }"
                " QCheckBox:hover { background-color: #f1f5f9; border-radius: 4px; }"
                " QCheckBox::indicator { width: 16px; height: 16px; }"
            )
            cb.stateChanged.connect(self._update_count)
            self.listLayout.insertWidget(self.listLayout.count() - 1, cb)
            self._checkboxes.append((cb, att.AttendeeId))

        self._update_count()

    def _filter_list(self, keyword: str):
        keyword = keyword.strip().lower()
        filtered = (
            self._all_available if not keyword
            else [a for a in self._all_available
                  if keyword in a.Name.lower() or keyword in a.Email.lower()]
        )
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
        if not self.get_selected_attendee_ids():
            QMessageBox.warning(self, "Error", "Please select at least one attendee!")
            return
        self.accept()

    def get_selected_attendee_ids(self) -> list:
        return [att_id for cb, att_id in self._checkboxes if cb.isChecked()]