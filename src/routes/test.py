import os
from datetime import datetime, date

from flask import render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from src import app, db
from src.models import User, Course, Role, Lesson, Material, Test, Question, Answer, Result, Attempt
from src.routes.general import has_authority, is_curr_user_creator, is_creator


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/create", methods=['GET', 'POST'])
@has_authority(['Admin', 'Teacher'])
@login_required
def create_test(course_id, lesson_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()

    if is_curr_user_creator(course_id):
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
        questions=questions,
        is_creator=is_creator(course_id)
    )


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/<test_id>/question/create", methods=['GET', 'POST'])
@has_authority(['Admin', 'Teacher'])
@login_required
def create_question(course_id, lesson_id, test_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()
    test_with_id = Test.query.filter(Test.id == test_id).first()

    if is_curr_user_creator(course_id):
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

                    if correct_answer_count != 0:
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


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/<test_id>/result", methods=['POST'])
@login_required
def test_check(course_id, lesson_id, test_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()
    test_with_id = Test.query.filter(Test.id == test_id).first()

    attempt = Attempt.query.filter(Attempt.user_id == current_user.id).filter(Attempt.test_id == test_id).first()
    if attempt is None:
        new_attempt = Attempt(
            test_id=test_id,
            user_id=current_user.id,
            count=1
        )
        db.session.add(new_attempt)
        db.session.commit()
    else:
        attempt_count = attempt.count
        new_attempt_count = attempt_count + 1
        Attempt.query.filter(Attempt.user_id == current_user.id).filter(Attempt.test_id == test_id).update(
            dict(count=new_attempt_count)
        )

    new_attempt_count = Attempt.query.filter(Attempt.user_id == current_user.id).filter(
        Attempt.test_id == test_id).first().count

    for question in test_with_id.question:
        for answer in question.answer:
            answer_with_id = Answer.query.filter(Answer.id == answer.id).first()
            answer_text = str(request.form.get(str(answer.id))).lower()

            if answer_with_id.a_type == "text":
                if answer_with_id.text == answer_text:
                    answer_val = answer_with_id.val
                else:
                    answer_val = 0
                res = Result(
                    result=answer_val,
                    attempt=new_attempt_count,
                    user_id=current_user.id,
                    answer_id=answer.id
                )
                db.session.add(res)
                db.session.commit()

            elif answer_with_id.a_type == "option":

                if answer_text == "on":
                    answer_val = answer_with_id.val
                    res = Result(
                        result=answer_val,
                        attempt=new_attempt_count,
                        user_id=current_user.id,
                        answer_id=answer.id
                    )
                    db.session.add(res)
                    db.session.commit()
                else:
                    answer_val = 0
                    res = Result(
                        result=answer_val,
                        attempt=new_attempt_count,
                        user_id=current_user.id,
                        answer_id=answer.id
                    )
                    db.session.add(res)
                    db.session.commit()
            else:
                res = Result(
                    result=0,
                    attempt=new_attempt_count,
                    user_id=current_user.id,
                    answer_id=answer.id
                )
                db.session.add(res)
                db.session.commit()

    return redirect(url_for(
        'result',
        course_id=course_id,
        lesson_id=lesson_id,
        test_id=test_id,
        attempt=new_attempt_count
    ))


@app.route("/courses/<course_id>/lesson/<lesson_id>/test/<test_id>/result/<attempt>", methods=['GET'])
@login_required
def result(course_id, lesson_id, test_id, attempt):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()
    test_with_id = Test.query.filter(Test.id == test_id).first()

    attempt_count = Attempt.query.filter(Attempt.user_id == current_user.id).filter(
        Attempt.test_id == test_id).first().count

    max_result = 0

    user_result = 0

    for question in test_with_id.question:
        max_result = max_result + question.max_val
        question_result = 0

        for answer in question.answer:
            answer_result = Result.query.filter(Result.user_id == current_user.id).filter(
                Result.answer_id == answer.id).filter(
                Result.attempt == attempt).first()
            question_result += answer_result.result

        if question_result < 0:
            question_result = 0
        user_result = user_result + question_result

    return render_template(
        "course/lesson/test/result.html",
        course=course_with_id,
        lesson=lesson_with_id,
        test=test_with_id,
        max_result=max_result,
        user_result=user_result,
        attempt_count=attempt_count,
        current_attempt=int(attempt)
    )
