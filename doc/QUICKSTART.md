# ⚡ HƯỚNG DẪN NHANH

## 🚀 Khởi Động Nhanh (5 phút)

### Bước 1: Cài Đặt
```bash
pip install PyQt6 qrcode[pil]
```

### Bước 2: Chạy
```bash
python main.py
```

### Bước 3: Sử Dụng
Chương trình đã có sẵn dữ liệu mẫu, bạn có thể thử ngay!

---

## 📖 Workflow Cơ Bản

### 🎯 Kịch Bản 1: Tổ Chức Sự Kiện Mới

1. **Tạo Sự Kiện**
   - Tab "Quản Lý Sự Kiện" → "Thêm Sự Kiện Mới"
   - Điền thông tin: Tên, Ngày, Giờ, Địa điểm
   - Click "Lưu"

2. **Thêm Người Tham Dự**
   - Tab "Người Tham Dự" → "Thêm Người Tham Dự"
   - Điền: Họ tên, Email, SĐT, Tổ chức
   - Click "Lưu"

3. **Đăng Ký Tham Dự**
   - Tab "Đăng Ký" → Chọn sự kiện
   - Click "Đăng Ký Người Tham Dự"
   - Chọn người và xác nhận
   - Nhận mã đăng ký (VD: ABC12345)

4. **Check-in Trong Ngày**
   - Tab "Check-in" → Chọn sự kiện
   - Nhập mã đăng ký → Click "Check-in"
   - Hoặc: Click "Tạo Mã QR" và quét

---

## 🎪 Ví Dụ Thực Tế

### Tổ Chức Workshop Python

**Thông tin sự kiện:**
- Tên: "Workshop Python cho Beginner"
- Ngày: 20/03/2026
- Giờ: 14:00
- Địa điểm: Phòng Lab A203

**Quy trình:**
1. Tạo sự kiện như trên
2. Thêm 30 học viên vào hệ thống
3. Đăng ký 30 học viên vào workshop
4. Gửi mã QR cho từng người qua email
5. Ngày workshop: Quét QR để check-in
6. Xem thống kê: 28/30 người đã check-in

---

## 💡 Tips Nhanh

### ⌨️ Shortcuts
- **Tìm kiếm nhanh:** Gõ trực tiếp vào ô search
- **Chọn hàng:** Click vào bảng
- **Làm mới:** F5 hoặc nút "Làm Mới"

### 🎯 Best Practices
1. **Thêm người tham dự trước** khi tạo sự kiện
2. **Check email trùng** khi thêm người mới
3. **Tạo QR code** ngay sau khi đăng ký
4. **Backup dữ liệu** thường xuyên (copy folder datasets)

### ⚠️ Lưu Ý
- Mã đăng ký **không phân biệt hoa/thường**
- Không thể check-in **2 lần** với cùng mã
- Xóa sự kiện sẽ **xóa tất cả đăng ký** liên quan
- Email phải **duy nhất** trong hệ thống

---

## 🔧 Troubleshooting Nhanh

### ❌ Lỗi: "Email đã tồn tại"
→ Người này đã có trong hệ thống, dùng chức năng tìm kiếm

### ❌ Lỗi: "Mã không hợp lệ"
→ Kiểm tra lại mã đăng ký, đảm bảo gõ đúng

### ❌ Lỗi: "Đã check-in trước đó"
→ Người này đã check-in rồi, xem tab Check-in để confirm

### ❌ Không hiển thị tiếng Việt
→ Kiểm tra encoding UTF-8, cài font tiếng Việt

---

## 📱 Demo Data

Chương trình có sẵn:
- **3 sự kiện** mẫu
- **5 người tham dự** mẫu  
- **4 đăng ký** (2 đã check-in, 2 chưa)

Bạn có thể:
- Xem, sửa, xóa dữ liệu mẫu
- Thêm dữ liệu mới
- Reset bằng cách xóa file JSON và restart

---

## 🎓 Video Hướng Dẫn

*(Sẽ cập nhật)*

1. Giới thiệu tổng quan (5 phút)
2. Quản lý sự kiện (3 phút)
3. Đăng ký và check-in (5 phút)
4. Tạo QR code (2 phút)
5. Xem thống kê (2 phút)

---

## 📞 Cần Hỗ Trợ?

1. Đọc **README.md** để biết chi tiết
2. Đọc **INSTALL.md** nếu gặp lỗi cài đặt
3. Kiểm tra **CHANGELOG.md** để biết tính năng mới

---

**Chúc bạn sử dụng hiệu quả!** 🎉

*Phiên bản: 1.0.0*  
*Cập nhật: 16/02/2026*
