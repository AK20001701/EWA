from flask_login import UserMixin

from src import db

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                     )

user_course = db.Table('user_course',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    path_to_img = db.Column(db.String(255), unique=True, nullable=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(100), unique=False, nullable=True)
    last_name = db.Column(db.String(100), unique=False, nullable=True)
    registration_date = db.Column(db.DATE, unique=False, nullable=False)

    roles = db.relationship('Role', secondary=user_role, lazy=False, backref=db.backref('users', lazy=True))
    courses = db.relationship('Course', secondary=user_course, lazy=False, backref=db.backref('courses', lazy=True))
    result = db.relationship('Result', backref='user', lazy=True)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=False)
    visible = db.Column(db.Boolean, unique=False, nullable=False)
    users = db.relationship('User', secondary=user_course, lazy=False, backref=db.backref('users', lazy=True))
    lessons = db.relationship('Lesson', backref='course', lazy=True)


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    test = db.relationship('Test', backref='lesson', lazy=True)
    material = db.relationship('Material', backref='lesson', lazy=True)


# add course img

# maybe add position column to control position of test/material by sorting quarry

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    t_type = db.Column(db.String(100), unique=False, nullable=False)
    exp_date = db.Column(db.DATE, nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    question = db.relationship('Question', backref='test', lazy=True)


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    file_name = db.Column(db.String(255), unique=False, nullable=False)
    extension = db.Column(db.String(120), unique=False, nullable=False)
    m_type = db.Column(db.String(100), unique=False, nullable=False)
    path_to_file = db.Column(db.String(255), unique=False, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False, nullable=False)
    max_val = db.Column(db.Float, unique=False, nullable=False)
    q_type = db.Column(db.String(100), unique=False, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    answer = db.relationship('Answer', backref='question', lazy=True)
    hint = db.relationship('Hint', backref='hint', lazy=True)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False, nullable=False)
    val = db.Column(db.Float, unique=False, nullable=False)
    a_type = db.Column(db.String(100), unique=False, nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    result = db.relationship('Result', backref='question', lazy=True)


class Hint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False, nullable=False)
    h_type = db.Column(db.String(100), unique=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Float, unique=False, nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), unique=False, nullable=False)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attended = db.Column(db.Boolean, unique=False, nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), unique=False, nullable=False)
