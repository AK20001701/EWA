import os

from flask import render_template, request, redirect, url_for, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename

from src import app, db
from src.models import Course, Lesson, Material
from src.routes.general import has_authority, is_curr_user_creator


@app.route("/courses/<course_id>/lesson/<lesson_id>/create/material", methods=['GET', 'POST'])
@has_authority(['Admin', 'Teacher'])
@login_required
def create_material(course_id, lesson_id):
    course_with_id = Course.query.filter(Course.id == course_id).first()
    lesson_with_id = Lesson.query.filter(Lesson.id == lesson_id).first()

    if is_curr_user_creator(course_id):
        if request.method == 'POST':
            material_name = request.form.get('material_name')

            file = request.files['file']
            filename = secure_filename(file.filename)
            if material_name == '':
                material_name = filename
            extension = os.path.splitext(filename)[1]
            m_type = extension

            prev_material_id = Material.query.filter(Material.lesson_id == lesson_id).order_by(Material.id).count()
            next_material_id = prev_material_id + 1
            filename = str(lesson_id) + '_' + str(next_material_id) + "_" + filename

            path_to_file = os.path.join(app.config['UPLOAD_FOLDER_MATERIAL'] + filename)
            file.save(path_to_file)

            new_material = Material(
                name=material_name,
                file_name=filename,
                extension=extension,
                m_type=m_type,
                path_to_file=path_to_file,
                lesson_id=lesson_id
            )
            db.session.add(new_material)
            db.session.commit()

            return redirect(url_for('lesson_home_page', course_id=course_id, lesson_id=lesson_id))
        else:
            return render_template("course/lesson/material/create.html", course=course_with_id, lesson=lesson_with_id)


@app.route("/courses/<course_id>/lesson/<lesson_id>/download/material/<material_id>")
@login_required
def download_material(course_id, lesson_id, material_id):
    material = Material.query.filter(Material.lesson_id == lesson_id).filter(Material.id == material_id).first()
    absolute_norm_path_to_file = os.path.normpath(os.getcwd() + material.path_to_file[1:])
    return send_file(
        absolute_norm_path_to_file,
        as_attachment=True,
        attachment_filename=material.name.replace(' ', '_') + material.extension
    )
