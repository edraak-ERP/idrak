# backend/app.py
from flask import Flask, render_template, request, jsonify
from models import init_db, Note
import utils

app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

# تهيئة قاعدة البيانات عند بدء تشغيل التطبيق
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        data = request.json
        # إذا أردت دعم التشفير، يمكنك استدعاء دالة utils.encrypt على المحتوى
        note = Note(title=data.get('title'), content=data.get('content'))
        note.save()
        return jsonify({'message': 'تم حفظ الملاحظة'}), 201
    else:
        notes = Note.get_all()
        return jsonify(notes), 200

@app.route('/api/notes/search', methods=['GET'])
def search_notes():
    query = request.args.get('q', '')
    results = Note.search(query)
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
