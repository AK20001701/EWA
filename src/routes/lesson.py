from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from src import app, db
from src.models import Course, Lesson, Material, Test
from src.routes.general import has_authority, is_curr_user_creator, is_creator


@app.route("/courses/<course_id>/lesson/create", methods=['GET', 'POST'])
@has_authority(['Admin', 'Teacher'])
@login_required
def create_lesson(course_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    if is_curr_user_creator(course_id):
        if request.method == 'POST':
            lesson_name = request.form.get('lesson_name')
            lesson_description = request.form.get('lesson_description')
            lesson_difficulty = request.form.get('lesson_difficulty')

            new_lesson = Lesson(
                name=lesson_name,
                description=lesson_description,
                difficulty=lesson_difficulty,
                course_id=course_id
            )
            db.session.add(new_lesson)
            db.session.commit()

            return redirect(url_for('course_home_page', course_id=course_id))
        else:
            return render_template("course/lesson/create.html", course=course_with_id)


@app.route("/courses/<course_id>/lesson/<lesson_id>")
@login_required
def lesson_home_page(course_id, lesson_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()

    materials = Material.query.filter(Material.lesson_id == lesson_id)
    tests = Test.query.filter(Test.lesson_id == lesson_id)

    return render_template(
        "course/lesson/homePage.html",
        course=course_with_id,
        lesson=lesson_with_id,
        materials=materials,
        tests=tests,
        is_creator=is_creator(course_id)
    )
