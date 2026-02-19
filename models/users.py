import json

from models.mycollections import MyCollections
from models.user import User


class Users(MyCollections):
    def import_json(self, filename):
        try:
            with open(filename, encoding='utf-8') as f:
                data = json.load(f)
                for p in data['users']:
                    it = User(
                        p['UserId'], p['FullName'], p['UserName'],
                        p['Password'], p['Email'], p.get('Role', 'user'),
                        p.get('SecurityQuestion', ''), p.get('SecurityAnswer', '')
                    )
                    self.add_item(it)
        except FileNotFoundError:
            pass

    def export_json(self, filename):
        data = {'users': []}
        for it in self.list:
            data['users'].append({
                'UserId': it.UserId,
                'FullName': it.FullName,
                'UserName': it.UserName,
                'Password': it.Password,
                'Email': it.Email,
                'Role': it.Role,
                'SecurityQuestion': it.SecurityQuestion,
                'SecurityAnswer': it.SecurityAnswer
            })
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def login(self, username, password):
        for it in self.list:
            if it.UserName == username and it.Password == password:
                return it
        return None

    def find_by_username(self, username):
        for it in self.list:
            if it.UserName == username:
                return it
        return None

    def find_by_email(self, email):
        for it in self.list:
            if it.Email.lower() == email.lower():
                return it
        return None

    def find_user(self, user_id):
        for it in self.list:
            if it.UserId == user_id:
                return it
        return None

    def update_user(self, user):
        exist = self.find_user(user.UserId)
        if exist is None:
            self.add_item(user)
        else:
            exist.FullName = user.FullName
            exist.UserName = user.UserName
            exist.Password = user.Password
            exist.Email = user.Email
            exist.Role = user.Role
            exist.SecurityQuestion = user.SecurityQuestion
            exist.SecurityAnswer = user.SecurityAnswer
        return True

    def delete_user(self, user_id):
        user = self.find_user(user_id)
        if user:
            self.list.remove(user)
            return True
        return False
