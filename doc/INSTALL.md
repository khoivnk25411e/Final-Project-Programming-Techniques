# HƯỚNG DẪN CÀI ĐẶT CHI TIẾT

## 📥 Cài Đặt Python

### Windows
1. Tải Python từ: https://www.python.org/downloads/
2. Chọn phiên bản Python 3.8 trở lên
3. **QUAN TRỌNG**: Check vào "Add Python to PATH"
4. Click "Install Now"

### macOS
```bash
# Sử dụng Homebrew
brew install python3
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

## 📦 Cài Đặt Thư Viện

### Cách 1: Sử dụng requirements.txt (Khuyến nghị)
```bash
# Di chuyển vào thư mục project
cd event_management

# Cài đặt tất cả thư viện
pip install -r requirements.txt
```

### Cách 2: Cài đặt từng thư viện
```bash
# PyQt6 (Bắt buộc)
pip install PyQt6

# QRCode (Tùy chọn - cho tính năng tạo QR)
pip install qrcode[pil]
```

## 🔍 Kiểm Tra Cài Đặt

Kiểm tra Python:
```bash
python --version
# hoặc
python3 --version
```

Kiểm tra PyQt6:
```bash
python -c "from PyQt6 import QtWidgets; print('PyQt6 OK')"
```

Kiểm tra qrcode:
```bash
python -c "import qrcode; print('QRCode OK')"
```

## 🚀 Chạy Chương Trình

### Windows
```bash
# Cách 1
python main.py

# Cách 2
python3 main.py
```

### macOS / Linux
```bash
# Cách 1
python3 main.py

# Cách 2
chmod +x main.py
./main.py
```

## ❗ Xử Lý Lỗi Thường Gặp

### Lỗi: "ModuleNotFoundError: No module named 'PyQt6'"
**Giải pháp:**
```bash
pip install PyQt6
```

### Lỗi: "python: command not found"
**Giải pháp:**
- Kiểm tra Python đã được cài đặt chưa
- Thêm Python vào PATH
- Thử dùng `python3` thay vì `python`

### Lỗi: "Permission denied"
**Giải pháp:**
```bash
# Windows: Chạy CMD/PowerShell với quyền Administrator
# Linux/Mac:
chmod +x main.py
```

### Lỗi: Không hiển thị tiếng Việt
**Giải pháp:**
- Đảm bảo file được lưu với encoding UTF-8
- Cài đặt font tiếng Việt

### Lỗi: Không tạo được QR code
**Giải pháp:**
```bash
pip install qrcode[pil]
pip install Pillow
```

## 🔧 Cài Đặt Trong Môi Trường Ảo (Khuyến nghị)

### Tạo môi trường ảo
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Cài đặt thư viện trong môi trường ảo
```bash
pip install -r requirements.txt
```

### Thoát môi trường ảo
```bash
deactivate
```

## 📂 Cấu Trúc File Sau Khi Cài Đặt

```
event_management/
├── models/
│   ├── __init__.py
│   ├── mycollections.py
│   ├── event.py
│   ├── events.py
│   ├── attendee.py
│   ├── attendees.py
│   ├── registration.py
│   └── registrations.py
├── ui/
│   ├── __init__.py
│   ├── MainWindow.py
│   ├── MainWindowEx.py
│   ├── EventDialog.py
│   ├── EventDialogEx.py
│   ├── AttendeeDialog.py
│   ├── AttendeeDialogEx.py
│   ├── RegistrationDialog.py
│   └── RegistrationDialogEx.py
├── datasets/
│   ├── events.json
│   ├── attendees.json
│   └── registrations.json
├── images/
├── main.py
├── requirements.txt
├── README.md
└── INSTALL.md
```

## 🎯 Kiểm Tra Hoàn Tất

Sau khi cài đặt xong, chạy chương trình:
```bash
python main.py
```

Bạn sẽ thấy:
- ✅ Cửa sổ chính hiển thị
- ✅ 4 tab: Quản Lý Sự Kiện, Người Tham Dự, Đăng Ký, Check-in
- ✅ Dữ liệu mẫu đã được load
- ✅ Giao diện tiếng Việt hiển thị đúng

## 📞 Hỗ Trợ

Nếu gặp vấn đề khi cài đặt:
1. Kiểm tra lại phiên bản Python (>= 3.8)
2. Đảm bảo pip đã được cập nhật: `pip install --upgrade pip`
3. Thử cài đặt trong môi trường ảo
4. Kiểm tra log lỗi và tìm giải pháp cụ thể

## 🔄 Cập Nhật

Để cập nhật thư viện:
```bash
pip install --upgrade PyQt6
pip install --upgrade qrcode
```

---

**Chúc bạn cài đặt thành công!** 🎉
