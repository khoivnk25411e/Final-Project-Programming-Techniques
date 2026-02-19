class Event:
    def __init__(self, EventId=None, EventName=None, EventDate=None, EventTime=None, Location=None, Description=None):
        self.EventId = EventId
        self.EventName = EventName
        self.EventDate = EventDate
        self.EventTime = EventTime
        self.Location = Location
        self.Description = Description
    
    def __str__(self):
        return f"{self.EventId}\t{self.EventName}\t{self.EventDate}\t{self.EventTime}\t{self.Location}"
