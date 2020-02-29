from app import app
from flask import jsonify, request, render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("hello.html")