from extensions import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    question = db.Column(db.String(255), nullable=False)

    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)

    correct_answer = db.Column(db.String(1), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(50))
    category = db.Column(db.String(50))
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)