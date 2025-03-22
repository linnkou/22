import os
import pytesseract
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
import numpy as np

# تحديد المسار إلى Tesseract إذا لزم الأمر
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

# مجلد لحفظ الصور المرفوعة
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "لم يتم العثور على الملف!"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "لم يتم اختيار أي ملف!"})

    # حفظ الملف
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # تشغيل OCR لاستخراج النص
    text = extract_text(filepath)
    return jsonify({"text": text})

def extract_text(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # تشغيل OCR
    text = pytesseract.image_to_string(img, lang="ara")
    return text.strip()

if __name__ == "__main__":
    app.run(debug=True)
