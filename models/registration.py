class Registration:
    def __init__(self, participant_id=None, event_id=None, register_time=None):
        self.participant_id = participant_id
        self.event_id = event_id
        self.register_time = register_time
        self.checkin_status=False
