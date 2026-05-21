from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "لا يوجد ملف"
    file = request.files['file']
    if file.filename == '':
        return "لم يتم اختيار ملف"
    file.save('temp.pdf')
    
    # استخراج النص
    text = ""
    with pdfplumber.open('temp.pdf') as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            
    return render_template('index.html', extracted_text=text)

@app.route('/generate', methods=['POST'])
def generate():
    # هنا ستأتي بيانات النموذج كاملة
    user_data = {
        "name": request.form.get('name'),
        "job_title": request.form.get('job_title'),
        "email": request.form.get('email'),
        "phone": request.form.get('phone'),
        "address": request.form.get('address'),
        "experiences": request.form.getlist('experience[]'),
        "skills": request.form.getlist('skills[]')
    }
    return render_template('result.html', data=user_data)

if __name__ == '__main__':
    app.run()
