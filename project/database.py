from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post = db.relationship('Group', backref='author', lazy=True)

    # def get_id(self):
    #     return (self.user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ref = db.relationship('Referal', backref='refer', lazy=True)

    def __repr__(self):
        return f"Group('{self.title}', '{self.created_date}')"

class Referal(db.Model):
    referal_code = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(100), db.ForeignKey('group.title'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Referal('{self.referal_code}', '{self.created_date}')"