from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # استخدام .get يوفر حماية من الخطأ إذا كان الحقل فارغاً
    user_data = {
        "name": request.form.get('name', 'غير محدد'),
        "job": request.form.get('job_title', 'غير محدد'),
        "objective": request.form.get('objective', ''),
        "experiences": request.form.getlist('experience[]'),
        "skills": request.form.getlist('skills[]')
    }
    return render_template('result.html', data=user_data)

if __name__ == '__main__':
    app.run()
