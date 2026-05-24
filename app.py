from flask import Flask, render_template, request, send_file
from openai import OpenAI
from weasyprint import HTML
import os

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # المعلومات الشخصية
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        city = request.form.get("city")
        address = request.form.get("address")
        linkedin = request.form.get("linkedin")

        # الوظيفة
        target_job = request.form.get("target_job")

        # التعليم
        university = request.form.get("university")
        major = request.form.get("major")
        graduation = request.form.get("graduation")

        # المهارات
        skills = request.form.get("skills")

        # الخبرات
        experience = request.form.get("experience")

        # اللغات
        languages = request.form.get("languages")

        # الدورات
        courses = request.form.get("courses")

        # قالب السيرة
        template = request.form.get("template")

        # الذكاء الاصطناعي
        prompt = f"""
        اكتب هدف وظيفي احترافي فقط لشخص يريد وظيفة:

        {target_job}

        وهذه خبراته:

        {experience}

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

            objective = response.choices[0].message.content

        except Exception as e:

            objective = "هدف وظيفي احترافي"

        # قالب حديث
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
            }}

            ul {{
                line-height: 2;
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
            {email} | {phone} | {city}
            </p>

            <p>
            {address}
            </p>

            <p>
            LinkedIn: {linkedin}
            </p>

            </div>

            <hr>

            <h2>الهدف الوظيفي</h2>

            <p>{objective}</p>

            <h2>التعليم</h2>

            <p>
            {university} - {major} - {graduation}
            </p>

            <h2>الخبرات</h2>

            <p>{experience}</p>

            <h2>المهارات</h2>

            <p>{skills}</p>

            <h2>اللغات</h2>

            <p>{languages}</p>

            <h2>الدورات</h2>

            <p>{courses}</p>

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
                font-family: Arial;
                direction: rtl;
            }}

            .card {{
                background: white;
                padding: 40px;
                border-radius: 15px;
            }}

            h1 {{
                color: #111827;
            }}

            h2 {{
                color: #2563eb;
            }}

            p {{
                line-height: 2;
            }}

            </style>

            </head>

            <body>

            <div class="card">

            <h1>{name}</h1>

            <p>{email} | {phone} | {city}</p>

            <hr>

            <h2>الهدف الوظيفي</h2>

            <p>{objective}</p>

            <h2>التعليم</h2>

            <p>{university} - {major} - {graduation}</p>

            <h2>الخبرات</h2>

            <p>{experience}</p>

            <h2>المهارات</h2>

            <p>{skills}</p>

            <h2>اللغات</h2>

            <p>{languages}</p>

            <h2>الدورات</h2>

            <p>{courses}</p>

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
