from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# تأكد من وجود مجلد للرفع
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "لم يتم رفع أي ملف"
    
    file = request.files['file']
    
    if file.filename == '':
        return "لم يتم اختيار أي ملف"
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # استخراج النصوص من الصورة
    text = pytesseract.image_to_string(Image.open(filepath), lang='ara')  # استخراج باللغة العربية

    return render_template('result.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)
