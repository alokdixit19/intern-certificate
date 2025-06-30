from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os
from certificate_generator import generate_certificate
import config
from send_mail import send_certificate

app = Flask(__name__)
app.secret_key = 'supersecret'
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

# MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

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
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO certificates (logo_path, name, course, start_date, end_date, email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (logo_path, name, course, start_date, end_date, email))
            mysql.connection.commit()

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
