#creating users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email    = email

    def __repr__(self):
        return "<User {}>".format(self.username)