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
            'title': thread_row['title'],
            'description': thread_row['description'],
            'perspectives': []
        }
        threads.append(thread)

        for perspective_row in the_db.table('perspectives').search(Query().thread_id == thread_row.doc_id):
            perspective = {
                'term': perspective_row['term'],
                'initial_interpretation': perspective_row['initial_interpretation'],
            }
            thread['perspectives'].append(perspective)

            for paraphrase_row in the_db.table('paraphrases').search(Query().perspective_id == perspective_row.doc_id):
                paraphrase = {
                    'paraphrase': paraphrase_row['paraphrase'],
                    'judgment': paraphrase_row.get('judgment')
                }

        #        perspective['paraphrases'].append(paraphrase)

    return render_template('wegetit.html', threads=threads)


@app.route('/threads', methods=['GET', 'POST'])
def post_thread():
    # insert new thread into DB, making a new id
    the_db = db.get_db()
    table = the_db.table('threads')
    if request.method == 'POST':
        thread_title = request.form.get('thread_title')
        thread_description = request.form.get('thread_description')
        error = None
        if not thread_title:
            error = 'Title is required.'
        if not thread_description:
            error = 'Description is required.'
        if error is not None:
            return(error)
        else:
            table.insert(
                {'title': thread_title, 'description': thread_description})
    # redirect(url_for('.threads'))
    return render_template('wegetit.html', threads=table)

    # TO DO: redirect to #thread_<id>
    # May need to add the following to the html: <script> $(function(){ window.location.hash = "jump_here"; }); </script>


@app.route('/threads/<int:thread_id>/perspectives', methods=['POST'])
def post_perspective(thread_id):
    # print(thread_id)
    the_db = db.get_db()
    threads = the_db.table('threads')
    table = the_db.table('perspectives')
    #thread_id = "thread_%s" % threads[doc_id]
    if request.method == 'POST':
        perspective_term = request.form.get('perspective_term')
        initial_interpretation = request.form.get(
            'initial_interpretation')
        error = None
        if not perspective_term:
            error = 'Term is required.'
#        if not perspective_definition:
#            error = 'Definition is required.'
        if error is not None:
            return(error)
        else:
            table.insert({'thread_id': thread_id, 'term': perspective_term,
                          'initial_interpretation': initial_interpretation})

    # redirect(url_for('perspectives'))
    return render_template('wegetit.html', threads=threads)
    # insert a new perspective into the DB, making a new id, and redirect to
    # #thread_<thread_id>_perspective_<id>


@app.route('/threads/<thread_id>/perspectives/<perspective_id>/paraphrases', methods=['POST'])
def post_paraphrase(thread_id, perspective_id):
    # print(thread_id)
    if request.method == 'POST':
        paraphrase = request.form.get('paraphrase')

    # insert a new paraphrase into the DB, making a new id, and redirect to
    # #thread_<thread_id>_perspective_<perspective_id>_paraphrase_<id>

    return 'ok'
