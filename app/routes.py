from app import app
from flask import jsonify, request, render_template

@app.route('/')
@app.route('/index')


def index():
    return render_template("hello.html")

@app.route('/user/<username>')
def user(username):
    user = {'username': 'susan'}
    # user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



