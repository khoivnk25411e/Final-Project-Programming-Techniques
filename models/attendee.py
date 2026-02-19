class Attendee:
    def __init__(self, AttendeeId=None, Name=None, Email=None, Phone=None, Organization=None, Position=None):
        self.AttendeeId = AttendeeId
        self.Name = Name
        self.Email = Email
        self.Phone = Phone
        self.Organization = Organization
        self.Position = Position
    
    def __str__(self):
        return f"{self.AttendeeId}\t{self.Name}\t{self.Email}\t{self.Phone}\t{self.Organization}\t{self.Position}"
