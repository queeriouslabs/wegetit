from tinydb import TinyDB, Query
import re

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = TinyDB('db.json')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db_tables = ['threads', 'perspectives', 'paraphrases']
    for db_table in db_tables:
        if db_table in db.tables():
            db.drop_table(db_table)

# threads: {"id": UID, "title" : String, "description" : String},
    table = db.table('threads')
    table.insert({'title': True, 'description': True})
    for row in table:
        print(row)

# perspectives: {"thread_id": FK_threads-id, "term" : String, "initial_interpretation" : String},
    table = db.table('perspectives')
    table.insert({'thread_id': True, 'term': True, 'initial_interpretation': True})
    for row in table:
        print(row)

# paraphrases: {"thread_id": FK_threads-id, "paraphrase" : String}
    table = db.table('paraphrases')
    table.insert({'perspective_id': True, 'paraphrase': True})
    for row in table:
        print(row)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
