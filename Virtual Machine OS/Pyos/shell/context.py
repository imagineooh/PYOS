class Context:
    def __init__(self):
        self.users={
            "flav":"CACA",
        }

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