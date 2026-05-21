from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # جمع البيانات
    user_data = {
        "name": request.form.get('name'),
        "job": request.form.get('job_title'),
        "experiences": request.form.getlist('experience[]'),
        "skills": request.form.getlist('skills[]')
    }
    # إرسال البيانات لصفحة التنسيق الاحترافي
    return render_template('result.html', data=user_data)

if __name__ == '__main__':
    app.run()
