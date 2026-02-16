class CheckinRecord:
    def __init__(self, participant_id=None, event_id=None,checkin_time=None,register_time=None,status=None):
        self.participant_id = participant_id
        self.event_id = event_id
        self.checkin_time = checkin_time
        self.register_time = register_time
        self.status = status