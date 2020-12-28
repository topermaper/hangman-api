import json
from random import choice
from app import app, db

class Game(db.Model):
    __tablename__ = 'tGame'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('tUser.id'))
    secret_word  = db.Column(db.String(20))
    score        = db.Column(db.Integer)
    multiplier   = db.Column(db.Integer)
    user_guess   = db.Column(db.String(25))
    misses       = db.Column(db.Integer)
    status       = db.Column(db.String(20))
    
    def __init__(self, user_id):
        self.secret_word = choice(app.config['WORD_LIST'])
        self.user_id     = user_id
        self.score       = 0
        self.multiplier  = 1
        self.user_guess  = ""
        self.misses      = 0
        self.status      = "ACTIVE"


    def __repr__(self):
        return "id:{}, status:{}, score:{}, user_guess:'{}', misses:{}, multiplier:x{}".format(self.id,self.status,self.score,self.user_guess,self.misses,self.multiplier)


    def serialize(self):
        return json.dumps({
            'id':self.id,
            'secret_word': self.secret_word,
            'score' : self.score,
            'multiplier' :self.multiplier,
            'user_guess' : self.user_guess_list,
            'misses' : self.misses,
            'status' :self.status
        },indent=4)