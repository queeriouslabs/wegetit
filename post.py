from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from wegetit.db import get_db

bp = Blueprint('post', __name__)

@bp.route('/')
def index():
    db = get_db()
#    threads = db.table('threads')
    return render_template('wegetit.html')
#    return render_template('post/wegetit.html', posts=threads)
