from flask import Flask, flash, render_template, request, redirect, url_for
import os
import db
from tinydb import TinyDB, Query
import sys

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'wegetit.tinydb'),
)
app.config['DEBUG'] = True
app.config['TESTING'] = True

ROOT_DIR = app.root_path


@app.route('/')
def root():
    the_db = db.get_db()
    threads = []
    for thread_row in the_db.table('threads').all():

        thread = {
            'id': thread_row.doc_id,
            'title': thread_row['title'],
            'description': thread_row['description'],
            'perspectives': []
        }
        threads.append(thread)

        for perspective_row in the_db.table('perspectives').search(Query().thread_id == thread_row.doc_id):
            perspective = {
                'id': perspective_row.doc_id,
                'term': perspective_row['term'],
                'initial_interpretation': perspective_row['initial_interpretation'],
                'paraphrases': []
            }
            thread['perspectives'].append(perspective)

            for paraphrase_row in the_db.table('paraphrases').search(Query().perspective_id == perspective_row.doc_id):
                paraphrase = {
                    'id': paraphrase_row.doc_id,
                    'paraphrase': paraphrase_row['paraphrase'],
                    'judgment': paraphrase_row.get('judgment')
                }

                perspective['paraphrases'].append(paraphrase)

    return render_template('wegetit.html', threads=threads)


@app.route('/threads', methods=['GET', 'POST'])
def post_thread():
    # insert new thread into DB, making a new id
    the_db = db.get_db()
    threads = the_db.table('threads')

    thread_title = request.form.get('thread_title')
    thread_description = request.form.get('thread_description')

    error = None
    if not thread_title:
        error = 'Title is required.'
    if not thread_description:
        error = 'Description is required.'

    if error is not None:
        return error

    thread_id = threads.insert(
        {'title': thread_title, 'description': thread_description})
    return redirect('/#thread_' + str(thread_id))


@app.route('/threads/<int:thread_id>/perspectives', methods=['POST'])
def post_perspective(thread_id):
    # insert new perspective into DB, making a new id
    the_db = db.get_db()
    threads = the_db.table('threads')
    perspectives = the_db.table('perspectives')

    perspective_term = request.form.get('perspective_term')
    initial_interpretation = request.form.get(
        'initial_interpretation')

    error = None
    if not perspective_term:
        error = 'Term is required.'

    if error is not None:
        return error

    perspective_id = perspectives.insert({'thread_id': thread_id, 'term': perspective_term,
                                          'initial_interpretation': initial_interpretation})

    return redirect('/#thread_' + str(thread_id) + '_perspective_' + str(perspective_id))


@app.route('/threads/<int:thread_id>/perspectives/<int:perspective_id>/paraphrases', methods=['POST'])
def post_paraphrase(thread_id, perspective_id):
    # insert a new paraphrase into the DB, making a new id, and redirect to

    the_db = db.get_db()
    threads = the_db.table('threads')
    perspectives = the_db.table('perspectives')
    paraphrases = the_db.table('paraphrases')

    paraphrase = request.form.get('paraphrase')

    error = None
    if not paraphrase:
        error = 'Paraphrase is required.'

    if error is not None:
        return error

    paraphrase_id = paraphrases.insert(
        {'perspective_id': perspective_id, 'paraphrase': paraphrase})

    return redirect('/#thread_' + str(thread_id) + '_perspective_' + str(perspective_id) + '_paraphrase_' + str(paraphrase_id))
