from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

from ui.QRScannerDialog import Ui_QRScannerDialog

try:
    import cv2
    from pyzbar import pyzbar
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False


class QRScannerDialogEx(Ui_QRScannerDialog):
    def __init__(self, parent=None, callback=None):
        """
        callback: hàm được gọi khi quét được mã QR
                  callback(qr_code_text) -> (success, message)
        """
        self.dialog = QDialog(parent)
        super().setupUi(self.dialog)
        self.callback = callback
        self.capture = None
        self.timer = QTimer()
        self.last_scanned = None  # Tránh quét trùng liên tục
        self.setupScanner()

    def setupScanner(self):
        if not SCANNER_AVAILABLE:
            self.videoLabel.setText(
                "⚠️ Thiếu thư viện!\n\n"
                "Cài đặt:\npip install opencv-python pyzbar"
            )
            return

        # Mở camera (0 = camera mặc định)
        self.capture = cv2.VideoCapture(0)
        
        if not self.capture.isOpened():
            self.videoLabel.setText(
                "❌ Không thể mở camera!\n\n"
                "Kiểm tra:\n"
                "- Camera đã kết nối chưa?\n"
                "- Ứng dụng khác đang dùng camera?"
            )
            return

        # Set resolution
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Start timer để đọc frame liên tục
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms = ~33 FPS

    def update_frame(self):
        """Đọc frame từ camera và quét QR code"""
        if self.capture is None or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        # Quét QR code
        decoded_objects = pyzbar.decode(frame)
        
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            
            # Tránh quét trùng liên tục cùng 1 mã
            if qr_data == self.last_scanned:
                continue
            
            self.last_scanned = qr_data
            
            # Vẽ khung xanh quanh QR code
            points = obj.polygon
            if len(points) == 4:
                pts = [(point.x, point.y) for point in points]
                for i in range(4):
                    cv2.line(frame, pts[i], pts[(i+1) % 4], (0, 255, 0), 3)

            # Gọi callback để check-in
            if self.callback:
                success, message = self.callback(qr_data)
                if success:
                    self.lblStatus.setStyleSheet(
                        "color: #27ae60; font-size: 13px; font-weight: bold; "
                        "padding: 8px; background: #d5f4e6; border-radius: 6px;"
                    )
                    self.lblStatus.setText(f"✅ {message}")
                else:
                    self.lblStatus.setStyleSheet(
                        "color: #e74c3c; font-size: 13px; font-weight: bold; "
                        "padding: 8px; background: #fadbd8; border-radius: 6px;"
                    )
                    self.lblStatus.setText(f"❌ {message}")
                
                self.lblStatus.setVisible(True)
                
                # Reset sau 3 giây để có thể quét mã mới
                QTimer.singleShot(3000, self.reset_scan)

        # Chuyển đổi frame sang QImage để hiển thị
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Hiển thị lên label
        pixmap = QPixmap.fromImage(qt_image)
        self.videoLabel.setPixmap(pixmap)

    def reset_scan(self):
        """Reset để có thể quét mã tiếp theo"""
        self.last_scanned = None
        self.lblStatus.setVisible(False)

    def closeEvent(self, event):
        """Đóng camera khi đóng dialog"""
        self.cleanup()
        event.accept()

    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        if self.timer.isActive():
            self.timer.stop()
        if self.capture is not None:
            self.capture.release()

    def exec(self):
        result = self.dialog.exec()
        self.cleanup()
        return result

    def reject(self):
        """Override reject để cleanup trước khi đóng"""
        self.cleanup()
        self.dialog.reject()
