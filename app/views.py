from flask import render_template
from app import app
import datetime

@app.route('/')
@app.route('/index')
def index():
    today = datetime.datetime.utcnow().strftime("%B %d, %Y")   # eg, February 11, 2016
    return render_template('index.html',
                           today = today)
