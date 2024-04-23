# app/views.py
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from .models import Document, db
import os

app_views = Blueprint('app_views', __name__)

@app_views.route('/')
def index():
    return render_template('upload_form.html')

@app_views.route('/upload', methods=['POST'])
def upload_document():
    file = request.files['document']
    title = request.form['title']
    author = request.form['author']
    date = request.form['date']
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        new_document = Document(title=title, author=author, date=date, filepath=filepath)
        db.session.add(new_document)
        db.session.commit()
        
        return redirect(url_for('app_views.document_detail', document_id=new_document.id))

@app_views.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        # Perform keyword-based search
        documents = Document.query.filter(Document.title.contains(query) | Document.author.contains(query)).all()
    else:
        # Retrieve all documents if no keyword is provided
        documents = Document.query.all()
    return render_template('search.html', documents=documents, query=query)

@app_views.route('/documents/<int:document_id>')
def document_detail(document_id):
    document = Document.query.get_or_404(document_id)
    return render_template('document_detail.html', document=document)
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
