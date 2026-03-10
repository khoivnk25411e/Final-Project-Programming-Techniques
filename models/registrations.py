import json
from datetime import datetime
from models.registration import Registration
from models.mycollections import MyCollections


class Registrations(MyCollections):
    def import_json(self, filename):
        try:
            with open(filename, encoding='utf-8') as json_file:
                data = json.load(json_file)
                for p in data['registrations']:
                    it = Registration(
                        p['RegistrationId'],
                        p['EventId'],
                        p['AttendeeId'],
                        p['RegistrationDate'],
                        p['Status'],
                        p.get('CheckinTime', None)
                    )
                    self.add_item(it)
        except FileNotFoundError:
            pass

    def export_json(self, filename):
        data = {'registrations': []}
        for it in self.list:
            data['registrations'].append({
                'RegistrationId': it.RegistrationId,
                'EventId': it.EventId,
                'AttendeeId': it.AttendeeId,
                'RegistrationDate': it.RegistrationDate,
                'Status': it.Status,
                'CheckinTime': it.CheckinTime
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def find_registration(self, regId):
        regId_upper = regId.strip().upper()
        for it in self.list:
            if it.RegistrationId.strip().upper() == regId_upper:
                return it
        return None

    def find_registration_by_event_attendee(self, eventId, attendeeId):
        for it in self.list:
            if it.EventId == eventId and it.AttendeeId == attendeeId:
                return it
        return None

    def get_registrations_by_event(self, eventId):
        results = []
        for it in self.list:
            if it.EventId == eventId:
                results.append(it)
        return results

    def delete_registration(self, regId):
        reg = self.find_registration(regId)
        if reg:
            self.list.remove(reg)
            return True
        return False

    def checkin(self, regId):
        reg = self.find_registration(regId)
        if reg:
            if reg.Status == "Checked-in":
                return False, "Already checked in previously"
            reg.Status = "Checked-in"
            reg.CheckinTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True, "Check-in successful"
        return False, "Registration not found"

    def count_registered_by_event(self, eventId):
        count = 0
        for it in self.list:
            if it.EventId == eventId:
                count += 1
        return count

    def count_checkedin_by_event(self, eventId):
        count = 0
        for it in self.list:
            if it.EventId == eventId and it.Status == "Checked-in":
                count += 1
        return count

    def delete_by_event(self, eventId):
        before = len(self.list)
        self.list = [r for r in self.list if r.EventId != eventId]
        return before - len(self.list)

    def delete_by_attendee(self, attendeeId):
        before = len(self.list)
        self.list = [r for r in self.list if r.AttendeeId != attendeeId]
        return before - len(self.list)

    def checkin_for_event(self, code, event_id):
        reg = self.find_registration(code)
        if reg is None:
            return False, f"Code not found: '{code}'\nMake sure you selected the correct event and entered the right code."
        if reg.EventId.strip() != event_id.strip():
            return False, f"This code belongs to a different event."
        if reg.Status == "Checked-in":
            return False, "This attendee has already checked in."
        from datetime import datetime
        reg.Status = "Checked-in"
        reg.CheckinTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True, f"✅ Check-in successful!"