# PHẦN MỀM QUẢN LÝ CHECK-IN SỰ KIỆN

Phần mềm quản lý sự kiện và check-in người tham dự sử dụng PyQt6 và JSON.

## 📋 TÍNH NĂNG

### 1. Quản Lý Sự Kiện
- ✅ Thêm sự kiện mới
- ✅ Cập nhật thông tin sự kiện
- ✅ Xóa sự kiện
- ✅ Xem danh sách và chi tiết sự kiện

### 2. Quản Lý Người Tham Dự
- ✅ Thêm người tham dự
- ✅ Cập nhật thông tin người tham dự
- ✅ Xóa người tham dự
- ✅ Tìm kiếm người tham dự (theo tên, email, SĐT, tổ chức)

### 3. Đăng Ký Tham Dự Sự Kiện
- ✅ Đăng ký người tham dự vào sự kiện
- ✅ Hủy đăng ký
- ✅ Xem danh sách đăng ký theo sự kiện
- ✅ Tạo mã QR cho đăng ký

### 4. Quản Lý Check-in
- ✅ Check-in bằng mã đăng ký
- ✅ Check-in bằng QR code
- ✅ Kiểm tra trùng check-in
- ✅ Ghi nhận thời gian check-in
- ✅ Xem danh sách đã check-in

### 5. Thống Kê - Báo Cáo
- ✅ Thống kê số người đăng ký
- ✅ Thống kê số người đã check-in
- ✅ Xem danh sách chưa check-in
- ✅ Thống kê theo từng sự kiện

### 6. Quản Lý Dữ Liệu
- ✅ Lưu dữ liệu tự động (JSON)
- ✅ Tải dữ liệu khi khởi động
- ✅ Sao lưu dữ liệu

## 🏗️ CẤU TRÚC THƯ MỤC

```
event_management/
├── models/                 # Các class model
│   ├── mycollections.py   # Base collection class
│   ├── event.py           # Model sự kiện
│   ├── events.py          # Collection sự kiện
│   ├── attendee.py        # Model người tham dự
│   ├── attendees.py       # Collection người tham dự
│   ├── registration.py    # Model đăng ký
│   └── registrations.py   # Collection đăng ký
│
├── ui/                     # Giao diện người dùng
│   ├── MainWindow.py      # UI chính
│   ├── MainWindowEx.py    # Logic xử lý chính
│   ├── EventDialog.py     # Dialog sự kiện
│   ├── EventDialogEx.py   # Logic xử lý sự kiện
│   ├── AttendeeDialog.py  # Dialog người tham dự
│   ├── AttendeeDialogEx.py # Logic xử lý người tham dự
│   ├── RegistrationDialog.py  # Dialog đăng ký
│   └── RegistrationDialogEx.py # Logic xử lý đăng ký
│
├── datasets/               # Dữ liệu JSON
│   ├── events.json        # Dữ liệu sự kiện
│   ├── attendees.json     # Dữ liệu người tham dự
│   └── registrations.json # Dữ liệu đăng ký
│
├── images/                 # Hình ảnh, icon
│
├── main.py                 # File chạy chương trình
└── README.md              # File hướng dẫn này
```

## 🚀 CÀI ĐẶT

### Yêu Cầu Hệ Thống
- Python 3.8 trở lên
- PyQt6
- qrcode (tùy chọn - cho tính năng tạo QR)

### Cài Đặt Thư Viện

```bash
# Cài đặt PyQt6
pip install PyQt6

# Cài đặt qrcode (tùy chọn)
pip install qrcode[pil]
```

## 💻 SỬ DỤNG

### Chạy Chương Trình

```bash
python main.py
```

### Hướng Dẫn Sử Dụng

#### 1. Quản Lý Sự Kiện
- Vào tab "📅 Quản Lý Sự Kiện"
- Click "➕ Thêm Sự Kiện Mới" để thêm sự kiện
- Chọn sự kiện trong bảng và click:
  - "👁 Xem Chi Tiết" để xem thông tin chi tiết
  - "✏ Cập Nhật" để sửa thông tin
  - "🗑 Xóa" để xóa sự kiện

#### 2. Quản Lý Người Tham Dự
- Vào tab "👥 Người Tham Dự"
- Sử dụng ô tìm kiếm để tìm người tham dự
- Click "➕ Thêm Người Tham Dự" để thêm mới
- Chọn người trong bảng và click:
  - "✏ Cập Nhật" để sửa thông tin
  - "🗑 Xóa" để xóa người tham dự

#### 3. Đăng Ký Sự Kiện
- Vào tab "📋 Đăng Ký"
- Chọn sự kiện từ dropdown
- Click "➕ Đăng Ký Người Tham Dự"
- Chọn người tham dự và xác nhận
- Mã đăng ký sẽ được tạo tự động
- Click "📱 Tạo Mã QR" để tạo QR code cho đăng ký

#### 4. Check-in
- Vào tab "✅ Check-in"
- Chọn sự kiện cần check-in
- Nhập mã đăng ký hoặc quét QR
- Click "✓ Check-in" để xác nhận
- Xem thống kê và danh sách đã check-in

## 📊 DỮ LIỆU MẪU

Chương trình đã có sẵn dữ liệu mẫu:
- 3 sự kiện
- 5 người tham dự
- 4 đăng ký (2 đã check-in, 2 chưa check-in)

## 🔧 TÍNH NĂNG KỸ THUẬT

### Kiến Trúc
- **MVC Pattern**: Tách biệt Model, View, Controller
- **JSON Storage**: Lưu trữ dữ liệu dạng JSON
- **PyQt6**: Framework GUI hiện đại
- **UUID**: Tạo ID duy nhất cho records

### Xử Lý Dữ Liệu
- Tự động load dữ liệu khi khởi động
- Tự động lưu khi có thay đổi
- Validate dữ liệu trước khi lưu
- Xử lý encoding UTF-8

### Giao Diện
- Responsive design
- Custom stylesheet
- Icon và emoji cho UX tốt hơn
- Thông báo rõ ràng

## 🐛 XỬ LÝ LỖI

Chương trình xử lý các trường hợp lỗi:
- File JSON không tồn tại → Tạo file mới
- Dữ liệu trùng lặp → Thông báo lỗi
- Input không hợp lệ → Validate và cảnh báo
- Check-in trùng → Thông báo đã check-in

## 📝 GHI CHÚ

- Tất cả dữ liệu được lưu trong thư mục `datasets/`
- Backup dữ liệu thường xuyên
- Mã đăng ký được tạo tự động (8 ký tự viết hoa)
- Thời gian được lưu theo định dạng: `YYYY-MM-DD HH:MM:SS`
- Ngày tháng hiển thị theo định dạng: `DD/MM/YYYY`

## 👨‍💻 PHÁT TRIỂN

Để mở rộng tính năng:
1. Thêm model mới vào thư mục `models/`
2. Tạo UI dialog trong thư mục `ui/`
3. Thêm xử lý logic vào `MainWindowEx.py`
4. Cập nhật file JSON tương ứng

## 📄 LICENSE

Phần mềm này được phát triển cho mục đích học tập và nghiên cứu.

## 📧 LIÊN HỆ

Nếu có vấn đề hoặc câu hỏi, vui lòng liên hệ qua email hoặc tạo issue.

---

**Phiên bản:** 1.0.0  
**Ngày phát hành:** 16/02/2026  
**Ngôn ngữ:** Python 3.8+  
**Framework:** PyQt6
