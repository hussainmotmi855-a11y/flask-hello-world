import os
import json
import pdfplumber
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def index():
    cv_data = None
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        file.save('temp.pdf')
        with pdfplumber.open('temp.pdf') as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        
        # الذكاء الاصطناعي يحلل البيانات
        prompt = f"استخرج البيانات التالية بتنسيق JSON: name, email, phone, job_title, education, skills, experience. النص: {text}"
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
        cv_data = json.loads(response.choices[0].message.content)
        
    return render_template('index.html', cv_data=cv_data)

if __name__ == '__main__':
    app.run()
