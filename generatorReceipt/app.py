from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Naloži okoljske spremenljivke
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Seznam podjetij in ustrezne predloge
COMPANIES = {
    "Apple": "email_apple.html",
    "Amazon": "email_amazon.html",
    "StockX": "email_stockx.html",
    "GOAT": "email_goat.html",
    "Ralph Lauren": "email_ralph.html",
    "Moncler": "email_moncler.html",
    "Dior": "email_dior.html",
    "About You": "email_aboutyou.html"
}

def send_email(receiver_email, data, template):
    """Pošlje HTML e-pošto brez priponke."""
    msg = EmailMessage()
    msg['Subject'] = f"Order Confirmation - {data['product_name']}"
    msg['From'] = EMAIL_USER
    msg['To'] = receiver_email

    # Ustvari HTML vsebino iz predloge
    html_content = render_template(f"emails/{template}", **data)
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        flash("✅ Order confirmation email sent successfully!", "success")
    except Exception as e:
        flash(f"❌ Error sending email: {str(e)}", "danger")

@app.route('/')
def index():
    """Prikazuje začetno stran z obrazcem za vnos podatkov"""
    return render_template('index.html', companies=COMPANIES.keys())

@app.route('/generate', methods=['POST'])
def generate():
    """Obdelava podatkov in pošiljanje e-pošte"""
    if request.method == 'POST':
        company = request.form['company']
        template = COMPANIES.get(company, "email_template.html")

        data = {
            "company": company,
            "product_name": request.form['product_name'],
            "order_date": request.form['order_date'],
            "price": request.form['price'],
            "img_url": request.form['img_url'],  # Dodano polje za sliko
            "full_name": request.form['full_name'],
            "address": f"{request.form['address']}, {request.form['city']}",
            "postcode": request.form['postcode'],
            "country": request.form['country'],
            "email": request.form['email']
        }

        send_email(data['email'], data, template)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
