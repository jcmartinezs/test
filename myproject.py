import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, current_app
from forms import ContactForm

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'myproject.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('MYPROJECT_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/', methods=['GET', 'POST'])
def contact():
    db = get_db()
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'error')
            return render_template('contact.html', form=form)
        else:
            try:
                db.execute('insert into entries (name, fvcolor, pet) values (?, ?, ?)',
                        [request.form['name'], request.form['fvcolor'], request.form['pet']])
            except sqlite3.Error as e:
                flash('Please do not repeat. New entry was not posted', 'error')
                return redirect(url_for('contact'))
            db.commit()
            flash('Thank you. New entry was successfully posted')
            return redirect(url_for('contact'))
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

