from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:qwerty1243@localhost:3306/ewadb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://gjnagtbgtvhczd:30ac7d0c0bd65d09212fe389c1f54c30dca8f807e67d82d573dc999a7eea7b27@ec2-54-247-89-181.eu-west-1.compute.amazonaws.com:5432/dct2kehbdqtefg'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '9y$B&E)H@McQfTjWnZr4u7x!z%C*F-JaNdRgUkXp2s5v8y/B?D(G+KbPeShVmYq3'
db = SQLAlchemy()
db.init_app(app)

app._static_folder = "../static"
app.config['UPLOAD_FOLDER_MATERIAL'] = './static/file/'
app.config['UPLOAD_FOLDER_IMAGE'] = './static/image/'

from src.models import User

manager = LoginManager(app)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from src import models

from src.routes import general, lesson, material, course, user, test

if False:
    from src.models import Role
    from werkzeug.security import generate_password_hash
    from datetime import datetime

    with app.app_context():
        db.create_all()
        print("Database created...")
        admin = Role(
            name="Admin"
        )
        teacher = Role(
            name="Teacher"
        )
        student = Role(
            name="Student"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin role added...")
        db.session.add(teacher)
        db.session.commit()
        print("Teacher role added...")
        db.session.add(student)
        db.session.commit()
        print("Student role added...")

        hash_password = generate_password_hash("q")
        new_user = User(
            login="q",
            email="q@q.q",
            password=hash_password,
            registration_date=datetime.date(datetime.now()),
            first_name="q",
            last_name="Q"
        )
        new_user.roles.append(Role.query.filter(Role.name == 'Admin').first())
        db.session.add(new_user)
        db.session.commit()

        hash_password = generate_password_hash("s")
        new_user = User(
            login="s",
            email="s@s.s",
            password=hash_password,
            registration_date=datetime.date(datetime.now()),
            first_name="s",
            last_name="S"
        )
        new_user.roles.append(Role.query.filter(Role.name == 'Student').first())
        db.session.add(new_user)
        db.session.commit()

        hash_password = generate_password_hash("at")
        new_user = User(
            login="at",
            email="at@at.at",
            password=hash_password,
            registration_date=datetime.date(datetime.now()),
            first_name="at",
            last_name="at"
        )
        new_user.roles.append(Role.query.filter(Role.name == 'Teacher').first())
        new_user.roles.append(Role.query.filter(Role.name == 'Admin').first())
        db.session.add(new_user)
        db.session.commit()
        print("Users added...")
        print("Data base configuration finished!")
