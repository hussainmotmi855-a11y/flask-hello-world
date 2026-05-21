import pdfplumber
from flask import Flask, render_template, request

app = Flask(__name__)

# دالة لاستخراج النص من PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "لا يوجد ملف"
    file = request.files['file']
    file.save('temp.pdf') # حفظ الملف مؤقتاً
    extracted_text = extract_text_from_pdf('temp.pdf')
    
    # هنا نقوم بإرسال النص المستخرج لصفحة النموذج ليعبأ الحقول تلقائياً
    return render_template('index.html', extracted_text=extracted_text)

if __name__ == '__main__':
    app.run()
