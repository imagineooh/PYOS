class Context:
    def __init__(self):
        self.users={
            "flav":"CACA",
        }
        self.signed_in=False

    def fetch(self):
        return self.users

    def login(self, username:str, password:str):
        if username in self.users:
            if self.users[username]==password:
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