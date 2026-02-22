# EVENT CHECK-IN MANAGEMENT SYSTEM

A comprehensive event management and check-in system built with PyQt6 and JSON storage, featuring user authentication, role-based access control, and QR code scanning capabilities.

## 📋 FEATURES

### 1. Event Management
- ✅ Create new events
- ✅ Update event information
- ✅ Delete events
- ✅ View event list and details

### 2. Attendee Management
- ✅ Add attendees
- ✅ Update attendee information
- ✅ Delete attendees
- ✅ Search attendees (by name, email, phone, organization)

### 3. Event Registration
- ✅ Register attendees for events
- ✅ Cancel registrations
- ✅ View registration list by event
- ✅ Generate QR codes for registrations

### 4. Check-in Management
- ✅ Check-in via registration code
- ✅ Check-in via QR code scanning (with camera)
- ✅ Prevent duplicate check-ins
- ✅ Record check-in timestamps
- ✅ View check-in list

### 5. Statistics & Reports
- ✅ Track number of registrations
- ✅ Track number of check-ins
- ✅ View list of non-checked-in attendees
- ✅ Export reports

### 6. User Authentication & Management
- ✅ Login system with remember me
- ✅ Forgot password with security questions
- ✅ Change password
- ✅ Role-based access (Admin/User)
- ✅ User account management (Admin only)

### 7. System Data Management
- ✅ Auto-save data (JSON)
- ✅ Load data on startup
- ✅ Data backup capabilities

## 🏗️ PROJECT STRUCTURE

```
event_management/
├── models/                 # Business logic & data models
│   ├── mycollections.py   # Base collection class
│   ├── event.py           # Event model
│   ├── events.py          # Event collection
│   ├── attendee.py        # Attendee model
│   ├── attendees.py       # Attendee collection
│   ├── registration.py    # Registration model
│   ├── registrations.py   # Registration collection
│   ├── user.py            # User model
│   └── users.py           # User collection
│
├── ui/                     # User interface components
│   ├── LoginWindow.py / LoginWindowEx.py           # Login screen
│   ├── ForgotPasswordDialog.py / Ex.py             # Forgot password
│   ├── ChangePasswordDialog.py / Ex.py             # Change password
│   ├── MainWindow.py / MainWindowEx.py             # Main window
│   ├── EventDialog.py / EventDialogEx.py           # Event dialog
│   ├── AttendeeDialog.py / AttendeeDialogEx.py     # Attendee dialog
│   ├── RegistrationDialog.py / Ex.py               # Registration dialog
│   ├── UserDialog.py / UserDialogEx.py             # User management dialog
│   ├── QRScannerDialog.py / QRScannerDialogEx.py   # QR scanner
│   └── *.ui                                         # Qt Designer UI files
│
├── datasets/               # JSON data storage
│   ├── events.json        # Event data
│   ├── attendees.json     # Attendee data
│   ├── registrations.json # Registration data
│   └── users.json         # User accounts
│
├── images/                 # Icons and images
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 INSTALLATION

### System Requirements
- Python 3.8 or higher
- PyQt6
- opencv-python (for QR scanning)
- pyzbar (for QR code decoding)
- qrcode (for QR generation)

### Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or install individually:
pip install PyQt6
pip install qrcode[pil]
pip install opencv-python
pip install pyzbar
```

## 💻 USAGE

### Running the Application

```bash
python main.py
```

### Default Accounts

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |
| `user01` | `user123` | User |
| `user02` | `user123` | User |

### User Roles

**Admin Role:**
- Full access to all features
- Can manage user accounts
- Can add/edit/delete events and attendees
- Can reset user passwords

**User Role:**
- View-only access to events and attendees
- Cannot add/delete events or attendees
- Can register attendees and perform check-ins
- Can change own password

### User Guide

#### 1. Login
- Enter username and password
- Check "Remember login" to save credentials
- Click "Forgot password?" if needed
- First-time users should change password after login

#### 2. Managing Events (Admin)
- Go to "📅 Event Management" tab
- Click "➕ Add New Event" to create events
- Select event and click "✏ Update" to edit
- Click "🗑 Delete" to remove events (will also delete related registrations)

#### 3. Managing Attendees
- Go to "👥 Attendees" tab
- Use search box to find attendees
- Click "➕ Add Attendee" to add new attendees
- Select attendee and click "✏ Update" or "🗑 Delete"

#### 4. Event Registration
- Go to "📋 Registration" tab
- Select event from dropdown
- Click "➕ Register Attendee"
- Select attendee and confirm
- Registration code will be generated automatically
- Click "📱 Generate QR" to create QR code for check-in

#### 5. Check-in
- Go to "✅ Check-in" tab
- Select event
- **Method 1:** Enter registration code manually
- **Method 2:** Click "📷 Scan QR" to use camera
  - Camera will open automatically
  - Hold QR code in front of camera
  - System will auto-detect and check-in
  - Green frame appears when QR is detected
- View statistics and check-in list in real-time

#### 6. Managing User Accounts (Admin Only)
- Go to "👤 Accounts" tab
- Click "➕ Add Account" to create new users
- Set role (Admin/User) and security question
- Click "✏ Update" to edit user information
- Click "🔑 Reset Password" to reset user's password
- Click "🗑 Delete" to remove users (cannot delete self)

#### 7. Changing Password
- Click "🔐 Change Password" button in header
- Enter current password
- Enter new password (minimum 6 characters)
- Confirm new password

#### 8. Forgot Password Recovery
- Click "Forgot password?" on login screen
- Enter username
- Answer security question
- Set new password

## 📊 SAMPLE DATA

The application includes sample data:
- **3 events** with different dates and locations
- **5 attendees** with complete information
- **4 registrations** (2 checked-in, 2 pending)
- **3 user accounts** (1 admin, 2 users)

You can:
- View, edit, or delete sample data
- Add your own data
- Reset by deleting JSON files and restarting

## 🔧 TECHNICAL FEATURES

### Architecture
- **MVC Pattern**: Separation of Model, View, Controller
- **JSON Storage**: Persistent data storage in JSON format
- **PyQt6**: Modern GUI framework
- **UUID**: Unique ID generation for records
- **Role-Based Access Control**: Admin/User permissions

### Data Handling
- Auto-load data on startup
- Auto-save on changes
- Data validation before saving
- UTF-8 encoding support for Vietnamese and international characters

### UI Features
- Responsive design
- Custom stylesheets
- Icons and emojis for better UX
- Clear notifications and feedback
- Tab-based navigation
- Real-time camera preview for QR scanning

### Security Features
- Password hashing (can be enhanced with bcrypt)
- Security questions for password recovery
- Session management
- Role-based feature access
- Cannot delete own admin account

## 🐛 ERROR HANDLING

The application handles common errors:
- Missing JSON files → Creates new files
- Duplicate data → Shows error message
- Invalid input → Validates and warns
- Duplicate check-ins → Prevents and notifies
- Camera access issues → Shows helpful error messages
- Missing libraries → Displays installation instructions

## 📝 NOTES

### Data Storage
- All data is stored in `datasets/` directory
- Backup data regularly by copying JSON files
- Registration codes are auto-generated (8 characters uppercase)
- Timestamps format: `YYYY-MM-DD HH:MM:SS`
- Dates display format: `DD/MM/YYYY`

### QR Code Scanning
- Requires webcam/camera access
- Default camera (index 0) is used
- Green frame indicates successful QR detection
- Prevents scanning same code twice within 3 seconds
- Auto-updates check-in list after successful scan

### Camera Permissions
- **Windows**: May need to grant camera access in Privacy settings
- **macOS**: Grant camera permission when prompted
- **Linux**: Ensure user has video device access

## 👨‍💻 DEVELOPMENT

### Adding New Features
1. Add model classes to `models/` directory
2. Create UI dialogs in `ui/` directory
3. Add logic handlers in `*Ex.py` files
4. Update corresponding JSON file structure

### Integration Ready
The system is designed for easy integration with:
- REST API
- Database systems (SQLite/MySQL/PostgreSQL)
- Email services
- SMS services
- Cloud storage
- Web interface

### Extending Functionality
Easy to add:
- New user roles
- Additional fields to models
- New report types
- Export formats (Excel, PDF)
- Email notifications
- SMS alerts
- Barcode scanning
- Badge printing

## 📄 LICENSE

This software is developed for educational and research purposes.

## 📧 SUPPORT

For issues or questions, please:
- Check the documentation
- Review sample code
- Create an issue in the repository

## 🔄 VERSION HISTORY

### Version 1.0.0
- ✅ Event management
- ✅ Attendee management
- ✅ Registration system
- ✅ Manual check-in
- ✅ QR code generation
- ✅ Statistics and reports
- ✅ User authentication system
- ✅ Role-based access control (Admin/User)
- ✅ Forgot password with security questions
- ✅ Change password functionality
- ✅ User account management
- ✅ QR code scanning with camera
- ✅ Auto-detect and check-in

## 🎯 FUTURE ENHANCEMENTS

### Planned for Version 1.1.0
- [ ] Export reports to Excel
- [ ] Export reports to PDF
- [ ] Email notifications
- [ ] CSV import
- [ ] Automatic backups
- [ ] Advanced search with filters
- [ ] Dashboard with charts
- [ ] Print attendance badges
- [ ] Multiple camera support
- [ ] Multi-language support

### Long-term Goals
- [ ] Database support (SQLite/MySQL)
- [ ] User permissions system
- [ ] Audit logs
- [ ] REST API
- [ ] Web interface
- [ ] Mobile app
- [ ] Cloud synchronization

## 🙏 ACKNOWLEDGMENTS

Built with:
- **PyQt6** - GUI Framework
- **OpenCV** - Camera and image processing
- **pyzbar** - QR code decoding
- **qrcode** - QR code generation
- **Pillow** - Image handling

---

**Version:** 1.1.0  
**Release Date:** February 16, 2026  
**Language:** Python 3.8+  
**Framework:** PyQt6  
**License:** Educational Use

**Status:** ✅ Production Ready

For more information, visit the project repository or contact the development team.