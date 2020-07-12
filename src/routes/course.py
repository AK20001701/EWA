import os
import uuid

from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from src import app, db
from src.models import Course, Lesson


@app.route("/courses")
def all_courses():
    search_text = request.args.get('course_name')
    if search_text == "" or search_text is None:
        selected_courses = Course.query.all()
    else:
        search = "%{}%".format(search_text)
        selected_courses = Course.query.filter(Course.name.like(search)).all()
    return render_template("course/all.html", courses=selected_courses)


@app.route("/courses/<course_id>")
@login_required
def show_course(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    enrolled = course_with_id in current_user.courses
    return render_template("course/info.html", course=course_with_id, enrolled=enrolled)


@app.route("/courses/create", methods=['GET', 'POST'])
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

        return redirect(url_for('all_courses'))
    else:
        return render_template("course/create.html")


@app.route("/courses/<course_id>/home")
@login_required
def course_home_page(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lessons = Lesson.query.filter(Lesson.course_id == course_id).all()

    return render_template("course/homePage.html", course=course_with_id, lessons=lessons)


@app.route("/courses/<course_id>/enroll")
@login_required
def enroll(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()

    print(current_user.courses)

    current_user.courses.append(course_with_id)

    print(current_user.courses)

    db.session.add(current_user)
    db.session.commit()

    return redirect(url_for("course_home_page", course_id=course_id))
