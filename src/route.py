from datetime import datetime

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from src import app, db
from src.models import User, Course


@app.route('/')
def welcome():
    return render_template("welcome.html")


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
            return render_template("login.html")
    else:
        return render_template("login.html")


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
        return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("welcome"))


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for("login_page"))
    return response


@app.route("/courses")
def all_courses():
    all_courses_from_db = Course.query.all()
    return render_template("courses.html", courses=all_courses_from_db)


@app.route("/courses/<course_id>")
@login_required
def show_course(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    return render_template("courseInfo.html", course=course_with_id)


@app.route("/courses/create", methods=['GET', 'POST'])
@login_required
def create_course():
    if request.method == 'POST':
        new_login = request.form.get('login_change')
    else:
        return render_template()




@app.route("/user", methods=['GET', 'POST'])
@login_required
def user_page():
    user_id = current_user.get_id()
    if request.method == 'POST':
        new_login = request.form.get('login_change')
        new_email = request.form.get('email_change')
        new_first = request.form.get('first_name_change')
        new_last = request.form.get('last_name_change')

        User.query.filter(User.id == user_id).update(
            dict(login=new_login, email=new_email, first_name=new_first, last_name=new_last)
        )
        db.session.commit()
        return redirect(url_for("user_page"))
    else:
        curr_user = User.query.filter(User.id == user_id).first()
        return render_template("user.html", user=curr_user)


@app.route('/test')
@login_required
def test():
    return render_template("test.html")
