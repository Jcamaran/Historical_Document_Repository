from flask import Blueprint, render_template, redirect, url_for, send_from_directory
from app.forms import UploadForm
from app.models import db, Document
import os

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return render_template("index.html")

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = file.filename
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        new_document = Document(title=filename, file_path=file_path)
        db.session.add(new_document)
        db.session.commit()
        return redirect(url_for('routes.home'))
    return render_template('upload.html', form=form)

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
