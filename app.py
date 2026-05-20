import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'hussain_secure_cv_key_2026'

# بيانات السيرة الذاتية لنظام الفرز ATS لـ الحسين مطمي
sample_cv = {
    'ar': {
        'name': 'الحسين يحيى مطمي',
        'title': 'محاسب مالي | متخصص في معايير المحاسبة الدولية',
        'summary': 'خريج محاسبة طموح يسعى لتطبيق مهاراته في التحليل المالي باستخدام Excel والمعايير الدولية لدعم استقرار المنشأة.',
        'education': 'دبلوم محاسبة - الكلية التقنية بأبها (2020م)',
        'skills': ['Microsoft Excel المتقدم', 'إعداد التقارير المالية', 'التحليل المالي', 'معايير القطاع العام IPSAS']
    },
    'en': {
        'name': 'Alhussain Yahya Motmi',
        'title': 'Financial Accountant | IPSAS Specialist',
        'summary': 'Accounting graduate seeking to apply financial analysis skills using Excel and international standards to support organizational stability.',
        'education': 'Accounting Diploma - College of Technology in Abha (2020)',
        'skills': ['Advanced Microsoft Excel', 'Financial Reporting', 'Financial Analysis', 'IPSAS Standards']
    }
}

PLATFORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="{{ lang }}" dir="{% if lang == 'ar' %}rtl{% else %}ltr{% endif %}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV Maker Pro</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 0; }
        .navbar { background: #0f172a; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; color: white; }
        .navbar a { color: #38bdf8; text-decoration: none; font-weight: bold; }
        .container { max-width: 1100px; margin: 40px auto; padding: 0 20px; }
        .hero { text-align: center; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 40px; }
        .section-title { font-size: 1.5em; color: #0f172a; border-bottom: 3px solid #0ea5e9; padding-bottom: 8px; margin-bottom: 25px; }
        .templates-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
        .template-card { background: white; border: 2px solid #e2e8f0; border-radius: 8px; overflow: hidden; transition: transform 0.2s; text-align: center; }
        .template-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        .template-preview { height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center; font-weight: bold; padding: 10px; }
        .template-preview.t1 { background: #f1f5f9; border-top: 5px solid #0f172a; }
        .template-preview.t2 { background: #fafafa; border-top: 5px solid #0ea5e9; }
        .template-preview.t3 { background: #f8fafc; border-top: 5px solid #16a085; }
        .card-body { padding: 20px; }
        .btn { background: #0ea5e9; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; font-weight: bold; width: 100%; box-sizing: border-box; }
    </style>
</head>
<body>
    <div class="navbar">
        <div style="font-size: 1.3em; font-weight: bold;">🚀 CV Maker Pro</div>
        <div><a href="/{% if lang == 'ar' %}en{% else %}ar{% endif %}">{% if lang == 'ar' %}English 🌐{% else %}العربية 🌐{% endif %}</a></div>
    </div>
    <div class="container">
        <div class="hero">
            <h1>{% if lang == 'ar' %}منظومة بناء السير الذاتية الاحترافية (ATS){% else %}Professional ATS CV Builder{% endif %}</h1>
            <p>{% if lang == 'ar' %}اختر من بين أفضل قوالب الـ ATS المتوافقة مع معايير الفرز الآلي للشركات{% else %}Select the best layout for your industry and preview your live CV{% endif %}</p>
        </div>
        <div class="section-title">{% if lang == 'ar' %}القوالب المدعومة بنظام فرز الشركات المباشر{% else %}Available Professional Templates{% endif %}</div>
        <div class="templates-grid">
            <div class="template-card">
                <div class="template-preview t1"><div style="color: #0f172a;">Executive Classic (النمط الكلاسيكي)</div></div>
                <div class="card-body"><a href="/view/1/{{ lang }}" class="btn">{% if lang == 'ar' %}معاينة القالب الكلاسيكي{% else %}Preview Template 1{% endif %}</a></div>
            </div>
            <div class="template-card">
                <div class="template-preview t2"><div style="color: #0ea5e9;">Modern Column (النمط الحديث المنظم)</div></div>
                <div class="card-body"><a href="/view/2/{{ lang }}" class="btn" style="background: #0ea5e9;">{% if lang == 'ar' %}معاينة القالب الحديث{% else %}Preview Template 2{% endif %}</a></div>
            </div>
            <div class="template-card">
                <div class="template-preview t3"><div style="color: #16a085;">Corporate Premium (النمط المالي المتقدم)</div></div>
                <div class="card-body"><a href="/view/3/{{ lang }}" class="btn" style="background: #16a085;">{% if lang == 'ar' %}معاينة القالب المالي{% else %}Preview Template 3{% endif %}</a></div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return redirect(url_for('home', lang='ar'))

@app.route('/<lang>')
def home(lang):
    if lang not in ['ar', 'en']: lang = 'ar'
    return render_template_string(PLATFORM_TEMPLATE, lang=lang)

@app.route('/view/<int:template_id>/<lang>')
def view_template(template_id, lang):
    data = sample_cv[lang]
    direction = 'rtl' if lang == 'ar' else 'ltr'
    
    if template_id == 1:
        html = f"""
        <div style="max-width: 800px; margin: 30px auto; background: white; padding: 40px; font-family: sans-serif; box-shadow: 0 0 10px rgba(0,0,0,0.05);" dir="{direction}">
            <h1 style="text-align: center; margin: 0; font-size: 28px;">{data['name']}</h1>
            <p style="text-align: center; color: #555; margin: 5px 0 20px 0; border-bottom: 2px solid #000; padding-bottom: 10px;">{data['title']}</p>
            <h3>الملخص المهني</h3><p>{data['summary']}</p>
            <h3>المؤهلات العلمية</h3><p>{data['education']}</p>
            <h3>المهارات الأساسية</h3><ul>""" + "".join([f"<li>{s}</li>" for s in data['skills']]) + "</ul></div>"
            
    elif template_id == 2:
        html = f"""
        <div style="max-width: 800px; margin: 30px auto; background: white; display: flex; font-family: sans-serif; box-shadow: 0 0 10px rgba(0,0,0,0.05);" dir="{direction}">
            <div style="width: 30%; background: #f1f5f9; padding: 30px 20px; border-top: 6px solid #0ea5e9;">
                <h3 style="color:#0ea5e9;">المهارات</h3>
                <ul style="padding: 0; list-style: none;">""" + "".join([f"<li style='margin-bottom:8px;'>🔹 {s}</li>" for s in data['skills']]) + f"""</ul>
            </div>
            <div style="width: 70%; padding: 30px;">
                <h1 style="margin:0; color:#0f172a;">{data['name']}</h1>
                <h4 style="color:#64748b; margin:5px 0 20px 0;">{data['title']}</h4>
                <h3 style="border-bottom:1px solid #e2e8f0; padding-bottom:5px;">النبذة التخصصية</h3><p>{data['summary']}</p>
                <h3 style="border-bottom:1px solid #e2e8f0; padding-bottom:5px;">التعليم</h3><p>{data['education']}</p>
            </div>
        </div>"""
        
    else:
        html = f"""
        <div style="max-width: 800px; margin: 30px auto; background: white; padding: 40px; font-family: sans-serif; border-top: 8px solid #16a085; box-shadow: 0 0 10px rgba(0,0,0,0.05);" dir="{direction}">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td>
                        <h1 style="margin: 0; color: #2c3e50;">{data['name']}</h1>
                        <div style="color: #16a085; font-weight: bold; margin-top: 5px;">{data['title']}</div>
                    </td>
                </tr>
            </table>
            <h3 style="background: #e8f8f5; color: #16a085; padding: 6px 10px; margin-top: 30px;">الملخص المهني</h3><p>{data['summary']}</p>
            <h3 style="background: #e8f8f5; color: #16a085; padding: 6px 10px;">المؤهل الدراسي</h3><p>{data['education']}</p>
            <h3 style="background: #e8f8f5; color: #16a085; padding: 6px 10px;">القدرات البرمجية والمالية</h3>""" + "".join([f"<span style='display:inline-block; background:#f4f7f6; padding:5px 12px; margin:5px; border-radius:4px; font-size:14px;'>✓ {s}</span>" for s in data['skills']]) + "</div>"
            
    back_btn = f'<div style="text-align:center; margin-top:20px;"><a href="/{lang}" style="background:#0f172a; color:white; padding:10px 20px; text-decoration:none; font-family:sans-serif; border-radius:5px;">⬅ العودة للقوالب الرئيسية</a></div>'
    return html + back_btn

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)