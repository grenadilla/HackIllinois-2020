from app import app
from flask import jsonify, request, render_template, redirect, flash, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, PurchaseForm
from app.models import User
from datetime import datetime
import requests
import json
from config import Config

@app.route('/')
@app.route('/index')
def index():
    return render_template("hello.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('basic_form.html', message='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    form = PurchaseForm()
    if form.validate_on_submit():
        post_request = {
            "merchant_id": form.merchant_id.data,
            "medium": "balance",
            "purchase_date": datetime.now().isoformat(),
            "amount": form.amount.data,
            "status": "pending",
            "description": form.description.id
        }

        json_request = json.dumps(post_request)
        payload = {'key': Config.API_KEY}
        response = requests.post(('{}accounts/{}/purchases').format(Config.API_URL, Config.API_ACCOUNT_ID), 
            params=payload, data=json_request, headers={'content-type': 'application/json'})

        if response.status_code == 200 or response.status_code == 201:
            flash('Purchase completed')
        else:
            json_response = json.loads(response.text)
            flash(('Error {}: {}: {}').format(json_response["code"], json_response["message"], 
                ','.join(json_response["culprit"])), 'error')

        return redirect(url_for('purchase'))

    return render_template('basic_form.html', message="Make Purchase", form=form)