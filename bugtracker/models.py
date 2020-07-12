from datetime import datetime
from bugtracker import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##############################################################################################################################

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.password}')"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(60), nullable=False)
    pitch = db.Column(db.String(500), nullable=False)
    bugs = db.relationship('Bug', backref='project', lazy=True)
    collaborators = db.relationship('Collaborator', backref='project', lazy=True)
    comments = db.relationship('Prcomment', backref='project', lazy=True)
    userid = db.Column(db.String(120), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.status}', '{self.date}', '{self.userid}')"

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    prid = db.Column(db.String(120), db.ForeignKey('project.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    prio = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(60), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    comments = db.relationship('Bugcomment', backref='bug', lazy=True)
    userid = db.Column(db.String(120), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.prid}', '{self.name}', '{self.date}', '{self.prio}', '{self.status}', '{self.userid}')"

class Collaborator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prid = db.Column(db.String(120), db.ForeignKey('project.id'), nullable=False)
    userid = db.Column(db.String(120), db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.prid}', '{self.userid}')"


class Prcomment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prid = db.Column(db.String(120), db.ForeignKey('project.id'), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.id}', '{self.prid}', '{self.comment}', '{self.date}')"

class Bugcomment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bugid = db.Column(db.String(120), db.ForeignKey('project.id'), nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.id}', '{self.bugid}', '{self.comment}', '{self.date}')"

##############################################################################################################################

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()