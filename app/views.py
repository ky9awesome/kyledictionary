from flask import render_template, redirect, request, url_for, flash
from app import app, db, models
import datetime


# helper functions
def get_date():
    return datetime.datetime.utcnow().strftime("%B %d, %Y") # eg, February 11, 2016

def get_time():
    return datetime.datetime.utcnow().strftime("%I:%M:%S%p") # eg, 2:23:46PM


# views
@app.route('/')
@app.route('/index')
def index():
    today = get_date()
    time = get_time()
    return render_template('_base.html',
                           today=today,
                           time=time)


@app.route('/new_entry')
def new_entry():
    today = get_date()
    time = get_time()
    return render_template('add_definition.html',
                           today=today,
                           time=time)


@app.route('/add', methods=['POST'])
def add():
    today = get_date()
    time = get_time()
    author = request.form['author']
    word = request.form['word']
    meaning = request.form['meaning']
    example = request.form['example']
    views = 0

    entry = models.Definition(author=author,
                              word=word,
                              meaning=meaning,
                              example=example,
                              views=views)

    db.session.add(entry)
    db.session.commit()

    flash('Thanks for your entry!')
    return redirect(url_for('index'))
