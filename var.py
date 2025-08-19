class rec:
    d = {}
    def __init__(self,user,password):
        self.user = user
        self.password = password
    def add_rec(self):
        rec.d[self.user] = self.password
        return "Succsessfull"
    def set_pass(self):
        return self.add_rec()


a = rec(123,123)
print(a.add_rec())