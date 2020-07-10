from datetime import datetime

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from src import app, db
from src.models import User


@app.route('/t')
def template():
    return render_template("template.html")


@app.route('/')
def welcome():
    return render_template("general/welcome.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        login = request.form.get('login_input')
        password = request.form.get('password_input')

        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for("welcome"))
        else:
            flash("Wrong email or password")
            return render_template("general/login.html")
    else:
        return render_template("general/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        login = request.form.get('login_input')
        email = request.form.get('email_input')
        password = request.form.get('password_input')
        password_rep = request.form.get('password_input_conf')
        new_user = ""
        if password != password_rep:
            flash("Wrong password or password confirmation!")
            return redirect(url_for('registration_page'))
        if not User.query.filter(User.email == email).first():
            hash_password = generate_password_hash(password)
            new_user = User(
                login=login,
                email=email,
                password=hash_password,
                registration_date=datetime.date(datetime.now())
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
        else:
            flash("User with this e-mail already exist!")
            return redirect(url_for('registration_page'))
    else:
        return render_template("general/register.html")


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for("login_page"))
    return response


@app.route('/test')
def test():
    return render_template("general/test.html")
