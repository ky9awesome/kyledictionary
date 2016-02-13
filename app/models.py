from app import db

class Definition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    word = db.Column(db.String(64), index=True)
    meaning = db.Column(db.String(1000))
    example = db.Column(db.String(1000))
    views = db.Column(db.Integer)
    votes_for = db.Column(db.Integer)
    votes_against = db.Column(db.Integer)

    def __repr__(self):
        return '<Definition %r>' % (self.word  + " : " + self.meaning)
