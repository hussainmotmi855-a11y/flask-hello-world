from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # هذا يوجه المستخدم لصفحة النموذج
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # هنا يستقبل البيانات من النموذج
    name = request.form.get('name')
    job = request.form.get('job_title')
    # يمكنك إضافة المزيد من الحقول هنا
    return f"تم استلام بيانات: {name} للمسمى: {job}"

if __name__ == '__main__':
    app.run()
