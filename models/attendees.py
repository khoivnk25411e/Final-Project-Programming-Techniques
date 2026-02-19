import json
from Event_Check_in_Management.models.attendee import Attendee
from Event_Check_in_Management.models.mycollections import MyCollections

class Attendees(MyCollections):
    def import_json(self, filename):
        try:
            with open(filename, encoding='utf-8') as json_file:
                data = json.load(json_file)
                for p in data['attendees']:
                    it = Attendee(
                        p['AttendeeId'],
                        p['Name'],
                        p['Email'],
                        p['Phone'],
                        p['Organization'],
                        p['Position']
                    )
                    self.add_item(it)
        except FileNotFoundError:
            pass
    
    def export_json(self, filename):
        data = {'attendees': []}
        for it in self.list:
            data['attendees'].append({
                'AttendeeId': it.AttendeeId,
                'Name': it.Name,
                'Email': it.Email,
                'Phone': it.Phone,
                'Organization': it.Organization,
                'Position': it.Position
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    
    def find_attendee(self, attendeeId):
        for it in self.list:
            if it.AttendeeId == attendeeId:
                return it
        return None
    
    def update_attendee(self, attendee):
        exist_attendee = self.find_attendee(attendee.AttendeeId)
        if exist_attendee is None:
            self.add_item(attendee)
            return True
        else:
            exist_attendee.Name = attendee.Name
            exist_attendee.Email = attendee.Email
            exist_attendee.Phone = attendee.Phone
            exist_attendee.Organization = attendee.Organization
            exist_attendee.Position = attendee.Position
            return True
    
    def delete_attendee(self, attendeeId):
        attendee = self.find_attendee(attendeeId)
        if attendee:
            self.list.remove(attendee)
            return True
        return False
    
    def search_attendees(self, keyword):
        results = []
        keyword_lower = keyword.lower()
        for it in self.list:
            if (keyword_lower in it.Name.lower() or
                keyword_lower in it.Email.lower() or
                keyword_lower in it.Phone.lower() or
                keyword_lower in it.Organization.lower() or
                keyword_lower in it.Position.lower()):
                results.append(it)
        return results
