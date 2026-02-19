import json
from models.event import Event
from models.mycollections import MyCollections

class Events(MyCollections):
    def import_json(self, filename):
        try:
            with open(filename, encoding='utf-8') as json_file:
                data = json.load(json_file)
                for p in data['events']:
                    it = Event(
                        p['EventId'], 
                        p['EventName'], 
                        p['EventDate'], 
                        p['EventTime'],
                        p['Location'],
                        p['Description']
                    )
                    self.add_item(it)
        except FileNotFoundError:
            pass
    
    def export_json(self, filename):
        data = {'events': []}
        for it in self.list:
            data['events'].append({
                'EventId': it.EventId,
                'EventName': it.EventName,
                'EventDate': it.EventDate,
                'EventTime': it.EventTime,
                'Location': it.Location,
                'Description': it.Description
            })
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    
    def find_event(self, eventId):
        for it in self.list:
            if it.EventId == eventId:
                return it
        return None
    
    def update_event(self, event):
        exist_event = self.find_event(event.EventId)
        if exist_event is None:
            self.add_item(event)
            return True
        else:
            exist_event.EventName = event.EventName
            exist_event.EventDate = event.EventDate
            exist_event.EventTime = event.EventTime
            exist_event.Location = event.Location
            exist_event.Description = event.Description
            return True
    
    def delete_event(self, eventId):
        event = self.find_event(eventId)
        if event:
            self.list.remove(event)
            return True
        return False
