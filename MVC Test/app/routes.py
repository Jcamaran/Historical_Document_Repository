# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
from .models import Document, db
import os

# Create a Blueprint named 'app_views'
app_views = Blueprint('app_views', __name__)

from .models import Document  # Move this import inside here if necessary, or leave it here if it works


@app_views.route('/')
def index():
    """ Render the main index page which acts as a landing page with links to other functionalities. """
    return render_template('base.html')

@app_views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['document']
        title = request.form['title']
        author = request.form['author']
        date = request.form['date']

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_document = Document(title=title, author=author, date=date, filepath=filepath)
            db.session.add(new_document)
            db.session.commit()

            return redirect(url_for('app_views.document_detail', document_id=new_document.id))

    return render_template('upload.html')

@app_views.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    documents = Document.query.filter(Document.title.contains(query) | Document.author.contains(query)).all()
    return render_template('search.html', documents=documents, query=query)

@app_views.route('/documents/<int:document_id>')
def document_detail(document_id):
    document = Document.query.get_or_404(document_id)
    return render_template('document_detail.html', document=document)

@app_views.route('/download/<int:document_id>')
def download_document(document_id):
    """ Serve the requested document file for download. """
    document = Document.query.get_or_404(document_id)
    return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], path=os.path.basename(document.filepath), as_attachment=True)

@app_views.route('/edit/<int:document_id>', methods=['GET', 'POST'])
def edit_document(document_id):
    document = Document.query.get_or_404(document_id)
    if request.method == 'POST':
        document.title = request.form['title']
        document.author = request.form['author']
        document.date = request.form['date']
        db.session.commit()
        return redirect(url_for('app_views.document_detail', document_id=document.id))

    return render_template('edit_document.html', document=document)

@app_views.route('/delete/<int:document_id>', methods=['POST'])
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], document.filepath))
    db.session.delete(document)
    db.session.commit()
    return redirect(url_for('app_views.search'))
