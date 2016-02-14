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
@app.route('/newest')
def index():
    today = get_date()
    time = get_time()
    newest_entries = models.Definition.query.order_by(models.Definition.timestamp.desc())
    description = "Newest entries:"
    return render_template('newest.html',
                           today=today,
                           time=time,
                           newest_entries=newest_entries)

@app.route('/popular')
def popular():
    today = get_date()
    time = get_time()
    popular_entries = models.Definition.query.order_by(models.Definition.votes_for - models.Definition.votes_against)
    description = "Most popular entries:"
    return render_template('popular.html',
                           today=today,
                           time=time,
                           popular_entries=popular_entries)


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
    timestamp = datetime.datetime.utcnow()

    entry = models.Definition(author=author,
                              word=word,
                              meaning=meaning,
                              example=example,
                              views=views,
                              timestamp=timestamp,
                              votes_for=0,
                              votes_against=0)

    db.session.add(entry)
    db.session.commit()

    flash('Thanks for your entry!')
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        q = request.form['search']
        return redirect(url_for('search_result',
                        q=q))
    return redirect(url_for('index'))


@app.route('/search/<q>')
def search_result(q):
    today = get_date()
    time = get_time
    results = models.Definition.query.filter_by(word=q).all()
    return render_template('search.html',
                           today=today,
                           time=time,
                           r=results,
                           query=q)

@app.route('/upvote/<int:record_id>/')
def upvote(record_id):
    record = models.Definition.query.filter_by(id=record_id).first()
    record.votes_for += 1

    db.session.add(record)
    db.session.commit()

    flash('Thanks for your vote!')
    return redirect(url_for('index'))

@app.route('/downvote/<int:record_id>/')
def downvote(record_id):
    record = models.Definition.query.filter_by(id=record_id).first()
    record.votes_against -= 1

    db.session.add(record)
    db.session.commit()

    flash('Thanks for your vote!')
    return redirect(url_for('index'))

