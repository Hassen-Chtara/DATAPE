from datetime import datetime
from DATAPE import db 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    password = db.Column(db.String(60), nullable=False)
    domain = db.relationship('Domain', backref='owner', lazy=True , cascade="all, delete-orphan")


    def __repr__(self):
    	return "{id:"+str(self.id)+",username:"+str(self.username)+"}"

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(120), unique=True, nullable=False)
    ip = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.relationship('Data', backref='of', lazy=True , cascade="all, delete-orphan")
    def __repr__(self):
        return "{id:"+str(self.id)+",name:"+str(self.name)+"}"

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), nullable=False)
    def __repr__(self):
    	return "{id:"+str(self.id)+",domain_id:"+str(self.domain_id)+"}"