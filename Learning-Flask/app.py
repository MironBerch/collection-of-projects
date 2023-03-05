import os 
import sqlite3

from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g


DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'f9sas99223112456'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    dict(
        DATABASE=os.path.join(
            app.root_path,
            'database.db'
        )
    )
)


def connect_db():
    connect = sqlite3.connect(
        app.config['DATABASE']
    )
    connect.row_factory = sqlite3.Row
    return connect


def create_db():
    db = connect_db()
    with app.open_resource('sql_database.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if not hasattr(g, 'link_db'):
        g.link_db.close()
    

@app.route('/index/')
@app.route('/')
def index():
    db = get_db()
    context = {'title': 'index'}
    return render_template('index.html', context=context)


@app.route('/contact/', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
        print(request.form['text'])
        if len(request.form['text']) < 2:
            flash('<2')
        else:
            flash('>2') 
    return render_template('contact.html')


@app.route('/user/<username>')
def user(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'{username}'


@app.errorhandler(404)
def error_404(error):
    return render_template('error.html', error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('user', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'miron' and request.form['password'] == '123':
        session['userLogged'] = request.form['username']
        print(session['userLogged'])
        return redirect(url_for('user', username=session['userLogged']))
    
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

#url_for('user', name='name') / url_for('index')