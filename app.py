from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv


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




@app.route('/')
def index():
    """Prikazuje začetno stran z obrazcem za vnos podatkov"""
    return render_template('index.html', companies=COMPANIES.keys())





# 🔹 Zagon aplikacije
if __name__ == '__main__':
    app.run(debug=True)
