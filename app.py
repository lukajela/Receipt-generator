from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import csv
from io import StringIO
from flask import Response

# 🔹 Naloži .env
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SECRET_KEY = os.getenv("SECRET_KEY") or "geslo"


# 🔹 Konfiguracija aplikacije
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receiptgen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 🔹 MODELI
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.Column(db.String(50))
    recipient_email = db.Column(db.String(120))
    product_name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 🔹 Seznam podjetij s predlogami in logotipi
COMPANIES = {
    "Apple": {
        "template": "email_apple.html",
        "logo": "https://1000logos.net/wp-content/uploads/2016/10/Apple-Logo-500x281.png",
        "from_name": "Apple Support"
    },
    "Amazon": {
        "template": "email_amazon.html",
        "logo": "https://1000logos.net/wp-content/uploads/2016/10/Amazon-Logo-500x281.png",
        "from_name": "Amazon Customer Service"
    },
    "Nike": {
        "template": "email_nike.html",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_NIKE.svg/1200px-Logo_NIKE.svg.png",
        "from_name": "Nike Customer Care"
    },
    "StockX": {
        "template": "email_stockx.html",
        "logo": "https://1000logos.net/wp-content/uploads/2023/11/StockX-Logo.png",
        "from_name": "StockX Team"
    },
    "GOAT": {
        "template": "email_goat.html",
        "logo": "https://logos-world.net/wp-content/uploads/2022/01/GOAT-Logo-700x394.png",
        "from_name": "GOAT Support"
    },
    "About You": {
        "template": "email_aboutyou.html",
        "logo": "https://images.seeklogo.com/logo-png/46/1/about-you-logo-png_seeklogo-461431.png",
        "from_name": "About You Customer Service"
    }
}

# 🔹 Home stran – samo za prijavljene
@app.route('/')
def index():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('index.html', companies=COMPANIES.keys())

# 🔹 Registracija
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# 🔹 Prijava
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Logged in successfully.", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password!", "danger")
    return render_template('login.html')

# 🔹 Odjava
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

# 🔹 Pošiljanje emaila
@app.route('/generate', methods=['POST'])
def generate():
    if "user_id" not in session:
        return redirect(url_for('login'))

    company = request.form['company']
    company_info = COMPANIES.get(company, {
        "template": "email_template.html",
        "logo": "",
        "from_name": "Customer Service"
    })

    data = {
        "company": company,
        "product_name": request.form['product_name'],
        "product_size": request.form['product_size'],
        "order_date": request.form['order_date'],
        "price": request.form['price'],
        "img_url": request.form['img_url'],
        "full_name": request.form['full_name'],
        "address": f"{request.form['address']}, {request.form['city']}",
        "postcode": request.form['postcode'],
        "country": request.form['country'],
        "email": request.form['email'],
        "processing_fee": "10.00",
        "logo_url": company_info["logo"]
    }

    # Email konfiguracija
    msg = EmailMessage()
    msg['Subject'] = f"Order Confirmation - {data['product_name']}"
    msg['From'] = f"{company_info['from_name']} <no-reply@services.com>"
    msg['To'] = data['email']
    msg.set_content("Thank you for your order!")
    html_content = render_template(f"emails/{company_info['template']}", **data)
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        # Log v bazo
        log = EmailLog(
            user_id=session["user_id"],
            company=company,
            recipient_email=data["email"],
            product_name=data["product_name"]
        )
        db.session.add(log)
        db.session.commit()

        flash("Email sent successfully!", "success")
    except Exception as e:
        flash(f"Email error: {str(e)}", "danger")

    return redirect(url_for('index'))

# 🔹 AJAX predogled emaila
@app.route('/preview', methods=['POST'])
def preview():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    company = request.form['company']
    company_info = COMPANIES.get(company, {"template": "email_template.html", "logo": "", "from_name": "Customer Service"})
    data = dict(request.form)
    data["logo_url"] = company_info["logo"]
    data["processing_fee"] = "10.00"
    html_content = render_template(f"emails/{company_info['template']}", **data)
    return html_content

@app.route('/logs', methods=['GET', 'POST'])
def logs():
    if "user_id" not in session:
        flash("You must be logged in to view logs.", "danger")
        return redirect(url_for('login'))

    user_id = session['user_id']
    company_filter = request.form.get("company")
    date_filter = request.form.get("date")

    logs_query = EmailLog.query.filter_by(user_id=user_id)

    if company_filter:
        logs_query = logs_query.filter_by(company=company_filter)
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, "%Y-%m-%d").date()
            logs_query = logs_query.filter(db.func.date(EmailLog.timestamp) == date_obj)
        except ValueError:
            flash("Invalid date format!", "danger")

    logs = logs_query.order_by(EmailLog.timestamp.desc()).all()

    companies = [log.company for log in EmailLog.query.with_entities(EmailLog.company).distinct()]
    return render_template("logs.html", logs=logs, companies=companies)

@app.route('/export_logs')
def export_logs():
    if "user_id" not in session:
        flash("You must be logged in to export logs.", "danger")
        return redirect(url_for('login'))

    logs = EmailLog.query.filter_by(user_id=session["user_id"]).order_by(EmailLog.timestamp.desc()).all()

    si = StringIO()
    writer = csv.writer(si, delimiter=';')  
    writer.writerow(['Datum', 'Podjetje', 'Prejemnik', 'Izdelek'])

    for log in logs:
        writer.writerow([
            log.timestamp.strftime('%d.%m.%Y %H:%M'),
            log.company,
            log.recipient_email,
            log.product_name
        ])

    output = si.getvalue()
    si.close()

    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=email_logs.csv'}
    )

@app.route('/logs/clear')
def clear_logs():
    if "user_id" not in session:
        flash("You must be logged in to clear logs.", "danger")
        return redirect(url_for('login'))

    EmailLog.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash("All logs deleted.", "success")
    return redirect(url_for('logs'))


# 🔹 Zagon aplikacije
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)