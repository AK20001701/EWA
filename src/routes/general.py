from datetime import datetime
from functools import wraps

from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from src import app, db
from src.models import User, Course, Role


def has_authority(roles):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for role in roles:
                if Role.query.filter(Role.name == role).first() in current_user.roles:
                    return func(*args, **kwargs)
            return abort(403)

        return wrapper

    return actual_decorator


def is_curr_user_creator(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    creators_of_course = course_with_id.creators
    if current_user in creators_of_course:
        return True
    else:
        return abort(403)


def is_creator(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    creators_of_course = course_with_id.creators
    return current_user in creators_of_course


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
            new_user.roles.append(Role.query.filter(Role.name == 'Student').first())
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
        else:
            flash("User with this e-mail already exist!")
            return redirect(url_for('registration_page'))
    else:
        return render_template("general/register.html")


@app.route('/about', methods=['GET'])
def about():
    return render_template("general/about.html")


@app.errorhandler(404)
def invalid_route(e):
    return render_template("error/fourZeroFourError.html")


@app.errorhandler(403)
def invalid_route(e):
    return render_template("error/fourZeroThreeError.html")


@app.errorhandler(500)
def invalid_route(e):
    return render_template("error/fiveZeroZero.html")


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for("login_page"))
    return response


@app.route('/test')
def test():
    return render_template("general/test.html")
