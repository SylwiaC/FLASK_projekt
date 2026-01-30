from flask import Flask, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import Question
import random
import os

print("APP STARTING...")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj-tajny-klucz-zmien-mnie'

ADMIN_PASSWORD = "Celebrini71"

# konfiguracja SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicjalizacja bazy
db.init_app(app)


# ============================
# STRONA STARTOWA
# ============================

@app.route('/')
def index():
    return render_template('index.html')


# ============================
# START QUIZU
# ============================

@app.route('/start/<category>')
def start_quiz(category):
    questions = Question.query.filter_by(category=category).all()
    random.shuffle(questions)

    session['question_ids'] = [q.id for q in questions]
    session['current'] = 0
    session['score'] = 0
    session['category'] = category

    return redirect(url_for('quiz'))


# ============================
# QUIZ
# ============================

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    if 'question_ids' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        q_id = session['question_ids'][session['current']]
        question = Question.query.get(q_id)

        if user_answer.lower() == question.correct_answer.lower():
            session['score'] += 1

        session['current'] += 1

        if session['current'] >= len(session['question_ids']):
            return redirect(url_for('result'))

    q_id = session['question_ids'][session['current']]
    question = Question.query.get(q_id)

    return render_template(
        'quiz.html',
        question=question,
        current=session['current'],
        total=len(session['question_ids'])
    )


# ============================
# WYNIK
# ============================

@app.route('/result')
def result():
    score = session.get('score', 0)
    total = len(session.get('question_ids', []))

    session.clear()
    return render_template('results.html', score=score, total=total)


# ============================
# DODAWANIE PYTAŃ
# ============================

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():

    if request.method == 'POST':
        password = request.form['password']

        if password != ADMIN_PASSWORD:
            flash("Błędne hasło admina!", "danger")
            return redirect(url_for('add_question'))

        category = request.form['category']
        question_text = request.form['question']

        q = Question(
            category=category,
            question=question_text,
            option_a=request.form['option_a'],
            option_b=request.form['option_b'],
            option_c=request.form['option_c'],
            option_d=request.form['option_d'],
            correct_answer=request.form['correct_answer'].upper()
        )

        db.session.add(q)
        db.session.commit()

        flash('Dodano pytanie!', 'success')
        return redirect(url_for('add_question'))

    return render_template('add_question.html')


# ============================
# START APLIKACJI
# ============================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
