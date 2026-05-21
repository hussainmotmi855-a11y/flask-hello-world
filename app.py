import os
from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "لا يوجد ملف"
    file = request.files['file']
    file.save('temp.pdf')
    
    text = ""
    with pdfplumber.open('temp.pdf') as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            
    return render_template('index.html', extracted_text=text)

@app.route('/generate', methods=['POST'])
def generate():
    user_data = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "phone": request.form.get('phone'),
        "job_title": request.form.get('job_title'),
        "education": request.form.get('education'),
        "experiences": request.form.getlist('experience[]'),
        "skills": request.form.getlist('skills[]')
    }
    return render_template('result.html', data=user_data)

if __name__ == '__main__':
    app.run()
