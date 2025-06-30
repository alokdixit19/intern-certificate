from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import psycopg2
import os
from certificate_generator import generate_certificate
from send_mail import send_certificate
import config

app = Flask(__name__)
app.secret_key = 'supersecret'
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

# PostgreSQL Connection Function
def get_connection():
    return psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        port=config.DB_PORT
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logo = request.files.get('logo')
        name = request.form.get('name')
        course = request.form.get('course')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        email = request.form.get('email')

        if logo and name and course and start_date and end_date and email:
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            logo.save(logo_path)

            # Save to DB
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO certificates (logo_path, name, course, start_date, end_date, email)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (logo_path, name, course, start_date, end_date, email))
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                return render_template('index.html', error="Database error: " + str(e), show_popup=True)

            # Generate PDF
            pdf_path = generate_certificate(logo_path, name, course, start_date, end_date)
            filename_only = os.path.basename(pdf_path)

            # Email certificate
            email_status = send_certificate(email, name, pdf_path)

            return render_template('index.html', download_file=filename_only, email_status=email_status, show_popup=True)

        return render_template('index.html', show_popup=True, error="Please fill out all fields.")
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join('static', 'certificates', filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
