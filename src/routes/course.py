from flask import render_template, request, redirect, url_for
from flask_login import login_required

from src import app, db
from src.models import Course, Lesson


@app.route("/courses")
def all_courses():
    all_courses_from_db = Course.query.all()
    return render_template("course/all.html", courses=all_courses_from_db)


@app.route("/courses/<course_id>")
@login_required
def show_course(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    return render_template("course/info.html", course=course_with_id)


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

        new_course = Course(
            name=course_name,
            description=course_description,
            visible=visible,
            rating=0
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



