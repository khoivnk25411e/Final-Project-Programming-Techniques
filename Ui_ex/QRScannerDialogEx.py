import os
import sys
import subprocess
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

from ui.QRScannerDialog import Ui_QRScannerDialog

IS_MACOS = sys.platform == "darwin"
if IS_MACOS:
    def _find_zbar_lib():
        candidates = [
            "/opt/homebrew/lib",
            "/usr/local/lib",
            "/opt/homebrew/opt/zbar/lib",
            "/usr/local/opt/zbar/lib",
        ]
        for path in candidates:
            if os.path.exists(os.path.join(path, "libzbar.dylib")):
                return path
        try:
            prefix = subprocess.check_output(
                ["brew", "--prefix", "zbar"], stderr=subprocess.DEVNULL
            ).decode().strip()
            lib_path = os.path.join(prefix, "lib")
            if os.path.exists(os.path.join(lib_path, "libzbar.dylib")):
                return lib_path
        except Exception:
            pass
        return None

    _zbar_path = _find_zbar_lib()
    if _zbar_path:
        _current = os.environ.get("DYLD_LIBRARY_PATH", "")
        if _zbar_path not in _current:
            os.environ["DYLD_LIBRARY_PATH"] = f"{_zbar_path}:{_current}"
# ─────────────────────────────────────────────────────────────────────────────

try:
    import cv2
    from pyzbar import pyzbar
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False


class QRScannerDialogEx(Ui_QRScannerDialog):
    def __init__(self, parent=None, callback=None):
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.callback = callback
        self.capture = None
        self.timer = QTimer()
        self.last_scanned = None

        # Fix vấn đề 6: gắn closeEvent đúng lên self.dialog
        self.dialog.closeEvent = self._on_close_event
        self.dialog.rejected.connect(self.cleanup)

        self.setupScanner()

    def setupScanner(self):
        if not SCANNER_AVAILABLE:
            self.videoLabel.setText(
                "⚠️ Missing libraries!\n\nInstall:\npip install opencv-python pyzbar\n"
                + ("brew install zbar" if IS_MACOS else "")
            )
            return

        if IS_MACOS:
            self.capture = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            if not self.capture.isOpened():
                self.capture = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
        else:
            self.capture = cv2.VideoCapture(0)

        if not self.capture.isOpened():
            msg = "❌ Unable to open camera!\n\nPlease check camera connection."
            if IS_MACOS:
                msg += "\n\n📌 macOS: System Settings → Privacy & Security → Camera\n→ Enable access for Terminal / Python"
            self.videoLabel.setText(msg)
            return

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        if self.capture is None or not self.capture.isOpened():
            return
        ret, frame = self.capture.read()
        if not ret:
            return

        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            if qr_data == self.last_scanned:
                continue
            self.last_scanned = qr_data

            points = obj.polygon
            if len(points) == 4:
                pts = [(p.x, p.y) for p in points]
                for i in range(4):
                    cv2.line(frame, pts[i], pts[(i + 1) % 4], (0, 255, 0), 3)

            if self.callback:
                success, message = self.callback(qr_data)
                if success:
                    self.lblStatus.setStyleSheet(
                        "color:#27ae60;font-size:13px;font-weight:bold;"
                        "padding:8px;background:#d5f4e6;border-radius:6px;"
                    )
                    self.lblStatus.setText(f"✅ {message}")
                else:
                    self.lblStatus.setStyleSheet(
                        "color:#e74c3c;font-size:13px;font-weight:bold;"
                        "padding:8px;background:#fadbd8;border-radius:6px;"
                    )
                    self.lblStatus.setText(f"❌ {message}")
                self.lblStatus.setVisible(True)
                QTimer.singleShot(3000, self.reset_scan)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        qt_image = QImage(frame_rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.videoLabel.setPixmap(QPixmap.fromImage(qt_image))

    def reset_scan(self):
        self.last_scanned = None
        self.lblStatus.setVisible(False)

    def _on_close_event(self, event):
        self.cleanup()
        event.accept()

    def cleanup(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.capture is not None:
            self.capture.release()
            self.capture = None

    def exec(self):
        result = self.dialog.exec()
        self.cleanup()
        return result

    def reject(self):
        self.cleanup()
        self.dialog.reject()