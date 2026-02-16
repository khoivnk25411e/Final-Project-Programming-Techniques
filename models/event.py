class Event:
    def __init__(self, Event_id=None, Event_Name=None, Date=None, Description=None, Location=None, Time=None, ):
        self.Event_id = Event_id
        self.Event_Name = Event_Name
        self.Date = Date
        self.Description = Description
        self.Location = Location
        self.Time = Time
        self.participants = []
    def __str__(self):
        infor = f"{self.Id}\t{self.Name}\t{self.Date}\t{self.Description}\t{self.Location}\t{self.Time}"
        return infor
