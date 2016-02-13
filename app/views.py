from flask import render_template
from app import app
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
