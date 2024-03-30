import sys
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

from tbt.auth import login_required
from tbt.db import get_db

bp = Blueprint('listing', 'tbt') # this is the blueprint that is specific to the textbook listings

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('listing/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    
    print('Inside create', file=sys.stderr)

    if request.method == 'POST':
        title = request.form['title']
        authors = request.form['authors']
        price = request.form['price']
        bk_condition = request.form['bk_condition']
        edition = request.form['edition']
        subject = request.form['subject']
        body = request.form['body']
        
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, price, bk_condition, authors, edition, subject)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (title, body, g.user['id'], price, bk_condition, authors, edition, subject)
            )
            db.commit()
            return redirect(url_for('listing.index'))

    return render_template('listing/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, price = ?, bk_condition = ?, authors = ?, edition = ?, subject = ?'
                ' WHERE id = ?',
                (title, body, id, price, bk_condition, authors, edition, subject)
            )
            db.commit()
            return redirect(url_for('listing.index'))

    return render_template('listing/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('listing.index'))


