class User:
    def __init__(self, UserId=None, FullName=None, UserName=None,
                 Password=None, Email=None, Role="user", SecurityQuestion=None, SecurityAnswer=None):
        self.UserId = UserId
        self.FullName = FullName
        self.UserName = UserName
        self.Password = Password
        self.Email = Email
        self.Role = Role                       # "admin" hoặc "user"
        self.SecurityQuestion = SecurityQuestion
        self.SecurityAnswer = SecurityAnswer

    def __str__(self):
        return f"{self.UserId}\t{self.FullName}\t{self.UserName}\t{self.Role}\t{self.Email}"
