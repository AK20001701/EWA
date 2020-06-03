from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:qwerty1243@localhost:3306/ewadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '9y$B&E)H@McQfTjWnZr4u7x!z%C*F-JaNdRgUkXp2s5v8y/B?D(G+KbPeShVmYq3'
db = SQLAlchemy()
db.init_app(app)

from src.models import User

manager = LoginManager(app)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from src import models, route

# from src.models import Role
# with app.app_context():
#     db.create_all()
#     admin = Role(
#         name="Admin"
#     )
#     teacher = Role(
#         name="Teacher"
#     )
#     student = Role(
#         name="Student"
#     )
#     db.session.add(admin)
#     db.session.commit()
#     db.session.add(teacher)
#     db.session.commit()
#     db.session.add(student)
#     db.session.commit()
