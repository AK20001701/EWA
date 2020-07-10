from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from src import app, db
from src.models import User, Role


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

        # curr_test_user = User.query.filter(User.id == user_id).first()
        # curr_test_user.roles.append(Role.query.filter(Role.name == 'Admin').first())

        db.session.commit()
        return redirect(url_for("user_page"))
    else:
        curr_user = User.query.filter(User.id == user_id).first()
        return render_template("user/homePage.html", user=curr_user)


# for admin only
@app.route("/user/all", methods=['GET'])
@login_required
def all_users():
    # curr_user_id = current_user.get_id()
    # curr_user = User.query.filter(User.id == curr_user_id).first()

    all_users_from_db = User.query.all()
    all_roles_from_db = Role.query.all()
    return render_template("user/all.html", users=all_users_from_db, roles=all_roles_from_db)


# for admin only
@app.route("/user/deleteUser", methods=['POST'])
@login_required
def delete_user():
    # curr_user_id = current_user.get_id()
    # curr_user = User.query.filter(User.id == curr_user_id).first()

    user_for_delete_id = request.form.get('userId')
    user_for_delete = User.query.filter(User.id == user_for_delete_id).first()

    db.session.delete(user_for_delete)
    db.session.commit()
    return redirect(url_for('all_users'))


# for admin only
@app.route("/user/changeRole", methods=['POST'])
@login_required
def change_user_role():
    # curr_user_id = current_user.get_id()
    # curr_user = User.query.filter(User.id == curr_user_id).first()

    user_for_change_id = request.form.get('userId')
    user_for_change_roles = request.form.getlist('roles')
    user_for_change = User.query.filter(User.id == user_for_change_id).first()

    user_for_change.roles = list()
    for role in user_for_change_roles:
        user_for_change.roles.append(Role.query.filter(Role.name == role).first())
    db.session.commit()
    return redirect(url_for('all_users'))
