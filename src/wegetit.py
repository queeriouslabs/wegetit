from flask import Flask, flash, make_response, render_template, request, redirect, url_for
import os
from tinydb import TinyDB, Query
import sys
import uuid

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
    user_uuid = request.cookies.get('user_uuid')
    generated_new_cookie = False
    if not user_uuid:
        user_uuid = str(uuid.uuid1())
        generated_new_cookie = True

    the_db = TinyDB(DB_FILE)
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
                'author': perspective_row['author'],
                'initial_interpretation': perspective_row['initial_interpretation'],
                'paraphrases': []
            }
            thread['perspectives'].append(perspective)

            for paraphrase_row in the_db.table('paraphrases').search(Query().perspective_id == perspective_row.doc_id):
                paraphrase = {
                    'id': paraphrase_row.doc_id,
                    'paraphrase': paraphrase_row['paraphrase'],
                    'judgment': paraphrase_row.get('judgment'),
                    'judgeable': user_uuid == perspective['author']
                }

                perspective['paraphrases'].append(paraphrase)

    resp = make_response(render_template('wegetit.html', threads=threads))
    if generated_new_cookie:
        resp.set_cookie('user_uuid', user_uuid)
    return resp


@app.route('/threads', methods=['GET', 'POST'])
def post_thread():
    user_uuid = request.cookies.get('user_uuid')
    generated_new_cookie = False
    if not user_uuid:
        user_uuid = str(uuid.uuid1())
        generated_new_cookie = True

    # insert new thread into DB, making a new id
    the_db = TinyDB(DB_FILE)
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

    thread_id = threads.insert({
        'title': thread_title,
        'description': thread_description
    })

    resp = make_response(redirect('/#thread_' + str(thread_id)))
    if generated_new_cookie:
        resp.set_cookie('user_uuid', user_uuid)
    return resp


@app.route('/threads/<int:thread_id>/perspectives', methods=['POST'])
def post_perspective(thread_id):
    user_uuid = request.cookies.get('user_uuid')
    generated_new_cookie = False
    if not user_uuid:
        user_uuid = str(uuid.uuid1())
        generated_new_cookie = True

    # insert new perspective into DB, making a new id
    the_db = TinyDB(DB_FILE)
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

    perspective_id = perspectives.insert({
        'thread_id': thread_id,
        'term': perspective_term,
        'author': user_uuid,
        'initial_interpretation': initial_interpretation
    })

    resp = make_response(
        redirect('/#thread_' + str(thread_id) + '_perspective_' + str(perspective_id)))
    if generated_new_cookie:
        resp.set_cookie('user_uuid', user_uuid)
    return resp


@app.route('/threads/<int:thread_id>/perspectives/<int:perspective_id>/paraphrases', methods=['POST'])
def post_paraphrase(thread_id, perspective_id):
    user_uuid = request.cookies.get('user_uuid')
    generated_new_cookie = False
    if not user_uuid:
        user_uuid = str(uuid.uuid1())
        generated_new_cookie = True

    # insert a new paraphrase into the DB, making a new id, and redirect to

    the_db = TinyDB(DB_FILE)
    threads = the_db.table('threads')
    perspectives = the_db.table('perspectives')
    paraphrases = the_db.table('paraphrases')

    paraphrase = request.form.get('paraphrase')

    error = None
    if not paraphrase:
        error = 'Paraphrase is required.'

    if error is not None:
        return error

    paraphrase_id = paraphrases.insert({
        'perspective_id': perspective_id,
        'paraphrase': paraphrase
    })

    resp = make_response(redirect('/#thread_' + str(thread_id) + '_perspective_' +
                                  str(perspective_id) + '_paraphrase_' + str(paraphrase_id)))
    if generated_new_cookie:
        resp.set_cookie('user_uuid', user_uuid)
    return resp


@app.route('/threads/<int:thread_id>/perspectives/<int:perspective_id>/paraphrases/<int:paraphrase_id>/they_get_it', methods=['GET'])
def get_they_get_it(thread_id, perspective_id, paraphrase_id):
    user_uuid = request.cookies.get('user_uuid')
    if user_uuid:
        # insert a new paraphrase into the DB, making a new id, and redirect to

        the_db = TinyDB(DB_FILE)
        threads = the_db.table('threads')
        perspectives = the_db.table('perspectives')
        paraphrases = the_db.table('paraphrases')

        paraphrases.update({'judgment': 'They get it! :)'},
                           doc_ids=[paraphrase_id])

    resp = make_response(redirect('/#thread_' + str(thread_id) + '_perspective_' +
                                  str(perspective_id) + '_paraphrase_' + str(paraphrase_id)))
    return resp


@app.route('/threads/<int:thread_id>/perspectives/<int:perspective_id>/paraphrases/<int:paraphrase_id>/they_dont_get_it', methods=['GET'])
def get_they_dont_get_it(thread_id, perspective_id, paraphrase_id):
    user_uuid = request.cookies.get('user_uuid')
    if user_uuid:
        # insert a new paraphrase into the DB, making a new id, and redirect to

        the_db = TinyDB(DB_FILE)
        threads = the_db.table('threads')
        perspectives = the_db.table('perspectives')
        paraphrases = the_db.table('paraphrases')

        paraphrases.update({'judgment': 'They don\'t get it. :('},
                           doc_ids=[paraphrase_id])

    resp = make_response(redirect('/#thread_' + str(thread_id) + '_perspective_' +
                                  str(perspective_id) + '_paraphrase_' + str(paraphrase_id)))
    return resp


def main(db_file):
    global DB_FILE

    if not db_file:
        print('Please provide a database file.')
        exit()

    DB_FILE = db_file
    return app
