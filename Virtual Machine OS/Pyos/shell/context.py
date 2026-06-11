class Context:
    def __init__(self):
        self.users={
            "user":["pass", 1],
        } #for now ima keep it like this lol, its not ready for actual production yet so just call that user ig
        self.signed_in=False

    def fetch(self):
        return self.users

    def login(self, username:str, password:str):
        if username in self.users:
            if self.users[username][0]==password:
                print('Authenticated with success! Loading TameOS...')
                return True
            else:
                print('Permission DENIED')
                return False
        else:
            print("Invalid Username")
    def signin(self):
        self.signed_in = True

    def is_in(self):
        if self.signed_in:
            return True

    def fetch_auth(self, user:str):
        return self.users[user][1]