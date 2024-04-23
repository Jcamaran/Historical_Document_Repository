from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app, flash
from werkzeug.utils import secure_filename
from .models import Document, db
from flask_login import login_required
from .permissions import admin_permission  # Ensure this is properly imported
import os

app_views = Blueprint('app_views', __name__)

@app_views.route('/')
@login_required
def index():
    # Display the base template upon login
    return render_template('base.html')

@app_views.route('/upload', methods=['GET', 'POST'])
@login_required
#@admin_permission.require(http_exception=403)  # Ensures only admins can upload
def upload():
    if request.method == 'POST':
        file = request.files['document']
        title = request.form['title']
        author = request.form['author']
        date = request.form['date']

        if file and file.filename:
            filename = secure_filename(file.filename)  # Sanitize the filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
                new_document = Document(title=title, author=author, date=date, filepath=filepath)
                db.session.add(new_document)
                db.session.commit()
                flash('Document uploaded successfully.', 'success')
                return redirect(url_for('app_views.document_detail', document_id=new_document.id))
            except Exception as e:
                flash(f'Failed to upload document: {str(e)}', 'danger')

    return render_template('upload.html')

@app_views.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    documents = Document.query.filter(Document.title.contains(query) | Document.author.contains(query)).all()
    return render_template('search.html', documents=documents, query=query)

@app_views.route('/documents/<int:document_id>')
@login_required
def document_detail(document_id):
    document = Document.query.get_or_404(document_id)
    return render_template('document_detail.html', document=document)

@app_views.route('/download/<int:document_id>')
@login_required
def download_document(document_id):
    document = Document.query.get_or_404(document_id)
    try:
        return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], path=os.path.basename(document.filepath), as_attachment=True)
    except FileNotFoundError:
        flash('The requested file does not exist.', 'danger')
        return redirect(url_for('app_views.document_detail', document_id=document_id))

@app_views.route('/edit/<int:document_id>', methods=['GET', 'POST'])
@login_required
#@admin_permission.require(http_exception=403)  # Admin only permission
def edit_document(document_id):
    document = Document.query.get_or_404(document_id)
    if request.method == 'POST':
        document.title = request.form['title']
        document.author = request.form['author']
        document.date = request.form['date']
        db.session.commit()
        flash('Document updated successfully.', 'success')
        return redirect(url_for('app_views.document_detail', document_id=document.id))

    return render_template('edit_document.html', document=document)

@app_views.route('/delete/<int:document_id>', methods=['GET', 'POST'])
@login_required
#@admin_permission.require(http_exception=403)  # Admin only permission
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    if request.method == 'POST':
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], document.filepath))
            db.session.delete(document)
            db.session.commit()
            flash('Document deleted successfully.', 'success')
        except Exception as e:
            flash(f'Failed to delete document: {str(e)}', 'danger')
        return redirect(url_for('app_views.search'))
    else:
        return render_template('delete_document.html', document=document)
