from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Naloži okoljske spremenljivke
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")  # Prijavni email (SMTP)
EMAIL_PASS = os.getenv("EMAIL_PASS")  # Geslo ali API ključ za SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 🔹 Seznam podjetij s pripadajočimi predlogami in logotipi
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

# 🔹 Funkcija za pošiljanje e-pošte
def send_email(receiver_email, data, company):
    """Pošlje HTML e-pošto z dinamičnimi podatki (logotip, pošiljatelj)."""

    # Pridobi informacije o podjetju (predloga, logotip, ime pošiljatelja)
    company_info = COMPANIES.get(company, {
        "template": "email_template.html",
        "logo": "",
        "from_name": "Customer Service"
    })

    msg = EmailMessage()
    msg['Subject'] = f"Order Confirmation - {data['product_name']}"
    msg['From'] = f"{company_info['from_name']} <no-reply@services.com>"  # 🔹 Vedno isti email, drugačno ime pošiljatelja
    msg['To'] = receiver_email
    msg['Reply-To'] = "support@services.com"  # 🔹 Če uporabnik odgovori, gre na ta email
    msg['List-Unsubscribe'] = '<mailto:unsubscribe@services.com>'  # 🔹 Izboljšana dostavljivost

    # 🔹 Dodamo logotip podjetja v podatke za e-poštno predlogo
    data["logo_url"] = company_info["logo"]

    # 🔹 Ustvarimo HTML in plain-text vsebino
    html_content = render_template(f"emails/{company_info['template']}", **data)
    plain_content = f"""
    Thank you for your order, {data['full_name']}.

    Order Details:
    Product: {data['product_name']}
    Price: {data['price']}
    Order Date: {data['order_date']}
    Address: {data['address']}

    If you have any questions, feel free to contact us.
    """

    msg.set_content(plain_content)  # 🔹 Dodamo navaden tekst
    msg.add_alternative(html_content, subtype="html")  # 🔹 Dodamo HTML verzijo

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        flash("✅ Order confirmation email sent successfully!", "success")
    except Exception as e:
        flash(f"❌ Error sending email: {str(e)}", "danger")

# 🔹 Prikaz začetne strani
@app.route('/')
def index():
    """Prikazuje začetno stran z obrazcem za vnos podatkov"""
    return render_template('index.html', companies=COMPANIES.keys())

# 🔹 Obdelava podatkov in pošiljanje e-pošte
@app.route('/generate', methods=['POST'])
def generate():
    """Obdelava podatkov in pošiljanje e-pošte"""
    if request.method == 'POST':
        company = request.form['company']
        company_info = COMPANIES.get(company, {
            "template": "email_template.html",
            "logo": "",
            "from_name": "Customer Service"
        })

        # 🔹 Zberemo vse podatke iz obrazca
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
            "logo_url": company_info["logo"]  # 🔹 Pošljemo pravi logotip
        }

        # 🔹 Pošljemo e-pošto s pravimi podatki
        send_email(data['email'], data, company)
        return redirect(url_for('index'))

# 🔹 Zagon aplikacije
if __name__ == '__main__':
    app.run(debug=True)
