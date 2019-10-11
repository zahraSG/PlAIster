from datetime import datetime
from dashboard import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader  # this is to specify a decorator
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # define a user with username and password and email adress. Only users can add devices to the device list
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Postdevice(db.Model):
    # make the device list for the posts and save in the SQLite database of Flask
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    crownID = db.Column(db.String(100), nullable=False)
    macAddress = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    endDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Postdevice('{self.name}', '{self.crownID}','{self.macAddress}', '{self.startDate}','{self.endDate}')"
