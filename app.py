import sqlite3
from flask import Flask, render_template, request
from werkzeug.exceptions import abort
import os
import logging

POSTS_PER_PAGE = 20
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))  # for absolute path
templates_dir = os.path.join(PROJECT_ROOT, 'templates')  # making folder with absolute path because of wsgi server
app = Flask(__name__, template_folder=templates_dir)
app.static_folder = os.path.join(PROJECT_ROOT, 'static')
db = os.path.join(PROJECT_ROOT, 'database.db')

print(f"Static folder: {app.static_folder}")
print(f"Template folder: {app.template_folder}")


def get_db_connection():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


# show unit
def get_unit(post_unit):
    conn = get_db_connection()
    units = conn.execute('SELECT * FROM posts WHERE Unit = ?',
                        (post_unit,)).fetchall()
    conn.close()
    if units is None:
        abort(404)
    return units


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


# show unit
@app.route('/unit/<post_unit>')
def unit(post_unit):
    print(f"Requested Post Units are: {post_unit}")
    units = get_unit(post_unit)
    return render_template('unit.html', posts=units)


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    conn = get_db_connection()
    total_posts = conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    total_pages = (total_posts // POSTS_PER_PAGE) + (1 if total_posts % POSTS_PER_PAGE > 0 else 0)
    offset = (page - 1) * POSTS_PER_PAGE
    posts = conn.execute('SELECT * FROM posts LIMIT ? OFFSET ?', (POSTS_PER_PAGE, offset)).fetchall()
    conn.close()
    print(f"Template folder: {app.template_folder}")
    logging.debug(f"Static folder: {app.static_folder}")
    return render_template('index.html', posts=posts, page=page, total_pages=total_pages)
