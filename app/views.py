from flask import render_template, redirect, request, url_for, flash
from app import app, db, models
from config import POSTS_PER_PAGE
import datetime


# helper functions
def get_date():
    return datetime.datetime.utcnow().strftime("%B %d, %Y") # eg, February 11, 2016

def get_time():
    return datetime.datetime.utcnow().strftime("%I:%M:%S%p") # eg, 2:23:46PM


# views
@app.route('/', methods=['GET', 'POST'])
@app.route('/newest', methods=['GET', 'POST'])
@app.route('/newest/<int:page>', methods=['GET', 'POST'])
def newest(page=1):
    today = get_date()
    time = get_time()
    newest_entries = models.Definition.query.order_by(models.Definition.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    description = "Newest entries:"
    return render_template('newest.html',
                           today=today,
                           time=time,
                           newest_entries=newest_entries)

@app.route('/popular', methods=['GET', 'POST'])
@app.route('/popular/<int:page>', methods=['GET', 'POST'])
def popular(page=1):
    today = get_date()
    time = get_time()
    popular_entries = models.Definition.query.order_by(models.Definition.votes_for.desc()).paginate(page, POSTS_PER_PAGE, True)
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
                              word=word.lower(),
                              meaning=meaning,
                              example=example,
                              views=views,
                              timestamp=timestamp,
                              votes_for=0,
                              votes_against=0)

    db.session.add(entry)
    db.session.commit()

    flash('Thanks for your entry!')
    return redirect(url_for('newest'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        q = request.form['search'].lower()
        return redirect(url_for('search_result',
                        q=q))
    return redirect(url_for('newest'))


@app.route('/search/<q>')
@app.route('/search/<q>/<page>')
def search_result(q, page=1):
    today = get_date()
    time = get_time
    results = models.Definition.query.filter_by(word=q).order_by(models.Definition.votes_for.desc()).paginate(page, POSTS_PER_PAGE, False)
    if results.items == []:
        return render_template('search.html',
                               today=today,
                               time=time,
                               callout=True,   # instead of showing results, invite user to add definition
                               query=q)
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
    return redirect(url_for('newest'))


@app.route('/downvote/<int:record_id>/')
def downvote(record_id):
    record = models.Definition.query.filter_by(id=record_id).first()
    record.votes_against -= 1

    db.session.add(record)
    db.session.commit()

    flash('Thanks for your vote!')
    return redirect(url_for('newest'))

