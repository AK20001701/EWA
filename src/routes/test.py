import os
from datetime import datetime, date

from flask import render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from src import app, db
from src.models import User, Course, Role, Lesson, Material, Test, Question, Answer, Result


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/create", methods=['GET', 'POST'])
@login_required
def create_test(course_id, lesson_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()

    if request.method == 'POST':
        test_name = request.form.get('test_name')
        test_type = request.form.get('test_type')
        exp_date = request.form.get('exp_date')
        exp_date = str(exp_date).split('.')
        exp_date = date(int(exp_date[2]), int(exp_date[1]), int(exp_date[0]))

        new_test = Test(
            name=test_name,
            t_type=test_type,
            exp_date=exp_date,
            lesson_id=lesson_id
        )
        db.session.add(new_test)
        db.session.commit()

        return redirect(url_for('lesson_home_page', course_id=course_id, lesson_id=lesson_id))
    else:
        return render_template("course/lesson/test/create.html", course=course_with_id, lesson=lesson_with_id)


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/<test_id>", methods=['GET', 'POST'])
@login_required
def test_home_page(course_id, lesson_id, test_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()
    test_with_id = Test.query.filter(Test.id == test_id).first()

    questions = Question.query.filter(Question.test_id == test_id).order_by(Question.id).all()

    return render_template(
        "course/lesson/test/homePage.html",
        course=course_with_id,
        lesson=lesson_with_id,
        test=test_with_id,
        questions=questions
    )


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/<test_id>/question/create", methods=['GET', 'POST'])
@login_required
def create_question(course_id, lesson_id, test_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()
    test_with_id = Test.query.filter(Test.id == test_id).first()

    if request.method == 'POST':
        question_text = request.form.get('question_text')
        max_val = request.form.get('max_val')
        q_type = request.form.get('question_type')

        new_question = Question(
            text=question_text,
            max_val=max_val,
            q_type=q_type,
            test_id=test_with_id.id
        )
        db.session.add(new_question)
        db.session.commit()

        if q_type == "option":
            count = int(request.form.get('count'))
            correct_answer_count = 0

            for i in range(1, count + 1):
                check_box = request.form.get('cb' + str(i))
                if check_box is not None:
                    correct_answer_count = correct_answer_count + 1

            for i in range(1, count + 1):
                check_box = request.form.get('cb' + str(i))
                answer_text = request.form.get('text' + str(i))

                answer_value = 0

                if check_box is not None:
                    answer_value = int(max_val) / correct_answer_count
                else:
                    answer_value = -int(max_val) / correct_answer_count

                new_answer = Answer(
                    text=answer_text,
                    val=answer_value,
                    a_type=q_type,
                    question_id=new_question.id
                )
                db.session.add(new_answer)
                db.session.commit()
        elif q_type == "text":
            answer_text = request.form.get('answer_text')
            new_answer = Answer(
                text=answer_text.lower(),
                val=max_val,
                a_type=q_type,
                question_id=new_question.id
            )
            db.session.add(new_answer)
            db.session.commit()

        return redirect(url_for(
            'test_home_page',
            course_id=course_id,
            lesson_id=lesson_id,
            test_id=test_id
        ))

    return render_template(
        "course/lesson/test/createQuestion.html",
        course=course_with_id,
        lesson=lesson_with_id,
        test=test_with_id
    )


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/<test_id>/result", methods=['GET', 'POST'])
@login_required
def get_result(course_id, lesson_id, test_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()
    test_with_id = Test.query.filter(Test.id == test_id).first()

    if request.method == 'POST':

        for question in test_with_id.question:
            for answer in question.answer:
                answer_with_id = Answer.query.filter(Answer.id == answer.id).first()
                answer_text = str(request.form.get(str(answer.id))).lower()

                if answer_with_id.a_type == "text":
                    if answer_with_id.text == answer_text:
                        answer_val = answer_with_id.val

                        result = Result(
                            result=answer_val,
                            user_id=current_user.id,
                            answer_id=answer.id
                        )
                        db.session.add(result)
                        db.session.commit()
                elif answer_with_id.a_type == "option":
                    if answer_text == "on":
                        answer_val = answer_with_id.val
                        result = Result(
                            result=answer_val,
                            user_id=current_user.id,
                            answer_id=answer.id
                        )
                        db.session.add(result)
                        db.session.commit()

        return redirect(url_for(
            'test_home_page',
            course_id=course_id,
            lesson_id=lesson_id,
            test_id=test_id
        ))

    return render_template(
        "course/lesson/test/result.html",
        course=course_with_id,
        lesson=lesson_with_id,
        test=test_with_id
    )
