import os
import json
import pdfplumber
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save('temp.pdf')
    
    # استخراج النص
    with pdfplumber.open('temp.pdf') as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    
    # توزيع البيانات ذكياً
    prompt = f"استخرج البيانات التالية من السيرة الذاتية بتنسيق JSON فقط: name, email, phone, job_title, education, skills, experience. النص: {text}"
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    
    try:
        cv_data = json.loads(response.choices[0].message.content)
    except:
        cv_data = {}
        
    return render_template('index.html', cv_data=cv_data)

if __name__ == '__main__':
    app.run()
