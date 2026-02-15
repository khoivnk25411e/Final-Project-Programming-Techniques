class Event:
    def __init__(self, Id=None, Name=None, Date=None, Description=None, Location=None, Time=None, ):
        self.Id = Id
        self.Name = Name
        self.Date = Date
        self.Description = Description
        self.Location = Location
        self.Time = Time
    def __str__(self):
        infor = f"{self.Id}\t{self.Name}\t{self.Date}\t{self.Description}\t{self.Location}\t{self.Time}"
        return infor
