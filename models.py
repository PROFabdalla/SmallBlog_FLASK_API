from app import db

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement='auto')
    title = db.Column(db.String(40),unique=True,nullable=False)
    age = db.Column(db.Integer(),nullable=False)

    def __init__(self,title):
        self.title = title