import sys
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from tbt.db import get_db

bp = Blueprint('auth', 'tbt', url_prefix='/auth') # this is a Flask object that authorizes views and code

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not email:
            error = 'Email is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), first_name, last_name, email),
                )
                db.commit()
                flash('Account created successfully', 'success')
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', showMin=True)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('auth/login.html', showMin=True)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/<int:id>/getuser')
@login_required
def getuser(id):
    return render_template('auth/account.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    print('Inside account create/update', file=sys.stderr)

    print('Request method type: ' + request.method, file=sys.stderr)

    if request.method == 'GET':
        return render_template('auth/account.html', updateMode=True)

    if request.method == 'POST':
        print('1', file=sys.stderr)
        first_name = request.form['first_name']
        print('1', file=sys.stderr)
        last_name = request.form['last_name']
        print('1', file=sys.stderr)
        error = None


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET first_name = ?, last_name = ?'
                ' WHERE id = ?',
                (first_name, last_name, session.get('user_id'))
            )
            db.commit()
            return redirect(url_for('listing.index'))

    return render_template('auth/account.html')