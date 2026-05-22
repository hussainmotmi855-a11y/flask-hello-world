import os
import json
import pdfplumber
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
# استخدام مفتاح الـ API من متغيرات البيئة (الأمان أولاً)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "لم يتم رفع ملف", 400
    file = request.files['file']
    file.save('temp.pdf')
    
    # استخراج النص
    with pdfplumber.open('temp.pdf') as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    
    # المعالجة الذكية
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "أعد البيانات بتنسيق JSON فقط: name, email, phone, job_title, education, skills, experience."},
                      {"role": "user", "content": text}]
        )
        data = json.loads(response.choices[0].message.content)
    except:
        data = {"error": "تعذر تحليل الملف بالذكاء الاصطناعي"}
        
    return render_template('index.html', cv_data=data)

if __name__ == '__main__':
    app.run()
