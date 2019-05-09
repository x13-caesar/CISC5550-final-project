import datetime, json
from flask import (Flask, g, render_template, flash, redirect, url_for, request)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
import requests

import models
import forms

app = Flask(__name__)
app.secret_key = "jasddbhA4576GJLKDSHHOAUI.3KSDFH_75"

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    resp = requests.post("http://35.185.36.225:5000/api/login_manager", json={
        "user_id": user_id})
    return resp


@app.before_request
def before_request():
    requests.put("http://35.185.36.225:5000/api/before")

@app.after_request
def after_request(response):
    requests.put("http://35.185.36.225:5000/api/after")
    return (response)


@app.route('/signup', methods=('GET', 'POST'))
def signup():
    resp = requests.put("http://35.185.36.225:5000/api/signup/")
    return resp


@app.route('/login', methods=('GET', 'POST'))
def login():
    resp = requests.put("http://35.185.36.225:5000/api/login/")
    return resp


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))

@app.route('/<int:user_id>/home')
@login_required
def main(user_id):
    resp = requests.get("http://35.185.36.225:5000/api/<int:user_id>/home")
    resp = resp.json()
    return render_template('home.html', todo=resp)

@app.route('/<int:user_id>/new_task', methods=('GET', 'POST'))
@login_required
def newTask(user_id):
    resp = requests.post("http://35.185.36.225:5000/api/<int:user_id>/new_task", json={
        "title": form.title.data, 
        "content": form.content.data,
        "priority": form.priority.data,
        "date": form.date.data,
        "user_id": user_id,
        "is_done": False})
    return resp

@app.route('/<int:user_id>/<int:task_id>/edit_task', methods=('GET', 'POST'))
@login_required
def editTask(user_id, task_id):
    resp = requests.post("http://35.185.36.225:5000/api/<int:user_id>/new_task", json={
        "user_id": user_id,
        "task_id": task_id})
    return resp

@app.route('/check', methods=('GET', 'POST'))
@login_required
def check_task():
    requests.post("http://35.185.36.225:5000/api/<int:user_id>/new_task", json={
        "data": int(request.form['task_id'])})
    return json.dumps({'status': 'OK'})

@app.route('/<int:user_id>/<int:task_id>/delete')
@login_required
def del_task(user_id, task_id):
    requests.post("http://35.185.36.225:5000/api/<int:user_id>/new_task", json={
        "data": task_id,
        "user_id": user_id})
    return redirect(url_for('main', user_id=user_id))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT, host=HOST)
