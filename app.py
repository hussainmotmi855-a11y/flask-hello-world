from flask import Flask, render_template, request, send_file
from openai import OpenAI
from weasyprint import HTML
import os

app = Flask(__name__)

# API KEY من Render Environment Variables
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        city = request.form.get("city")
        job = request.form.get("job")
        skills = request.form.get("skills")
        experience = request.form.get("experience")
        template = request.form.get("template")

        prompt = f"""
        أنشئ سيرة ذاتية احترافية ATS باللغة العربية.

        البيانات:

        الاسم: {name}
        البريد الإلكتروني: {email}
        رقم الهاتف: {phone}
        المدينة: {city}
        الوظيفة المستهدفة: {job}

        المهارات:
        {skills}

        الخبرة:
        {experience}

        المطلوب:

        - إنشاء هدف وظيفي احترافي
        - تنظيم المهارات
        - تحسين الخبرات
        - تنسيق احترافي
        - لا تستخدم markdown
        - استخدم HTML فقط
        """

        try:

            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response.choices[0].message.content

        except Exception as e:
            return f"خطأ في الذكاء الاصطناعي: {str(e)}"

        # قالب احترافي
        if template == "modern":

            html = f"""
            <html dir="rtl">

            <head>

            <meta charset="UTF-8">

            <style>

            body {{
                font-family: Arial;
                direction: rtl;
                padding: 40px;
                color: #111827;
            }}

            h1 {{
                color: #2563eb;
                margin-bottom: 5px;
            }}

            h2 {{
                color: #1d4ed8;
                border-bottom: 2px solid #2563eb;
                padding-bottom: 5px;
                margin-top: 25px;
            }}

            p {{
                line-height: 2;
                font-size: 15px;
            }}

            .top {{
                margin-bottom: 30px;
            }}

            </style>

            </head>

            <body>

            <div class="top">

            <h1>{name}</h1>

            <p>
            {email} |
            {phone} |
            {city}
            </p>

            </div>

            <hr>

            {content}

            </body>

            </html>
            """

        # قالب بسيط
        else:

            html = f"""
            <html dir="rtl">

            <head>

            <meta charset="UTF-8">

            <style>

            body {{
                background: #f3f4f6;
                padding: 40px;
                direction: rtl;
                font-family: Arial;
            }}

            .card {{
                background: white;
                padding: 40px;
                border-radius: 15px;
            }}

            h1 {{
                color: #111827;
            }}

            p {{
                line-height: 2;
            }}

            </style>

            </head>

            <body>

            <div class="card">

            <h1>{name}</h1>

            <p>
            {email} |
            {phone} |
            {city}
            </p>

            <hr>

            {content}

            </div>

            </body>

            </html>
            """

        # إنشاء PDF
        HTML(string=html).write_pdf("cv.pdf")

        return send_file(
            "cv.pdf",
            as_attachment=True
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
