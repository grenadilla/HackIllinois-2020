from app import app
from flask import jsonify, request, render_template
import pl

@app.route('/')
@app.route('/index')
def index():
    return render_template("hello.html")

@app.route('/request')
def request():
    return pl.purchase_data();
