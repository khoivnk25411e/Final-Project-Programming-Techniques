from datetime import datetime

class Registration:
    def __init__(self, RegistrationId=None, EventId=None, AttendeeId=None, RegistrationDate=None, Status="Đã đăng ký", CheckinTime=None):
        self.RegistrationId = RegistrationId
        self.EventId = EventId
        self.AttendeeId = AttendeeId
        self.RegistrationDate = RegistrationDate if RegistrationDate else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.Status = Status
        self.CheckinTime = CheckinTime
    
    def __str__(self):
        return f"{self.RegistrationId}\t{self.EventId}\t{self.AttendeeId}\t{self.Status}"
