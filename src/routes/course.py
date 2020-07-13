import os
import uuid

from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user, AnonymousUserMixin
from werkzeug.utils import secure_filename

from src import app, db
from src.models import Course, Lesson, Role
from src.routes.general import has_authority, is_creator


@app.route("/courses")
def all_courses():
    if current_user.is_authenticated:
        ability_to_add_new_courses = Role.query.filter(
            Role.name == "Teacher").first() in current_user.roles or Role.query.filter(
            Role.name == "Admin").first() in current_user.roles
    else:
        ability_to_add_new_courses = False

    search_text = request.args.get('course_name')
    if search_text == "" or search_text is None:
        selected_courses = Course.query.all()
    else:
        search = "%{}%".format(search_text)
        selected_courses = Course.query.filter(Course.name.like(search)).all()
    return render_template("course/all.html", courses=selected_courses, is_teacher=ability_to_add_new_courses)


@app.route("/courses/my")
def my_courses():
    return render_template("course/myCourses.html", myCourses=current_user.courses)


@app.route("/courses/<course_id>")
@login_required
def show_course(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    enrolled = course_with_id in current_user.courses
    return render_template("course/info.html", course=course_with_id, enrolled=enrolled)


@app.route("/courses/create", methods=['GET', 'POST'])
@has_authority(['Admin', 'Teacher'])
@login_required
def create_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_description = request.form.get('description')
        visible = request.form.get('visible')

        if visible:
            visible = True
        else:
            visible = False

        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename == "" or filename is None:
            filename = "course.png"
        else:
            filename = str(uuid.uuid4()) + "_" + filename
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER_IMAGE'] + filename)
            file.save(path_to_file)

        new_course = Course(
            name=course_name,
            description=course_description,
            visible=visible,
            rating=0,
            image_name=filename
        )
        db.session.add(new_course)
        db.session.commit()

        current_user.created_courses.append(new_course)
        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('all_courses'))
    else:
        return render_template("course/create.html")


@app.route("/courses/<course_id>/home")
@login_required
def course_home_page(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lessons = Lesson.query.filter(Lesson.course_id == course_id).all()

    return render_template(
        "course/homePage.html",
        course=course_with_id,
        lessons=lessons,
        is_creator=is_creator(course_id)
    )


@app.route("/courses/<course_id>/enroll")
@login_required
def enroll(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()

    current_user.courses.append(course_with_id)
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for("course_home_page", course_id=course_id))
