# 🧾 ReceiptGenerator

ReceiptGenerator je spletna aplikacija, ki omogoča uporabnikom generiranje in pošiljanje realističnih potrditvenih e-poštnih sporočil v imenu znanih podjetij (Apple, Amazon, Nike, StockX, GOAT ...). Namenjena je testiranju, simulacijam in demonstracijam.

---

## 🚀 Ključne funkcionalnosti

- ✅ Prijava in registracija uporabnikov
- ✅ En brezplačen poizkus (free trial)
- ✅ Plačilni sistem (Stripe) za neomejeno uporabo
- ✅ Uporabniški status (trial/premium) prikazan na nadzorni plošči
- ✅ Generiranje emailov z Jinja2 predlogami in SMTP pošiljanje
- ✅ Predogled emailov pred pošiljanjem (AJAX)
- ✅ Shranjevanje vseh poslanih emailov (logs)
- ✅ CSV izvoz logov
- ✅ Možnost brisanja vseh logov
- ✅ Preprost in odziven uporabniški vmesnik

---

## 🧑‍💻 Za koga je?

🎯 **Ciljna skupina:**
- Mladi in ustvarjalci vsebin (14–25 let)
- Uporabniki, ki pripravljajo spletne predstavitve ali teste UX
- Marketing agencije za pripravo demonstracij

---

## 💸 Poslovni model

- **Brezplačno:** 1 poslan email
- **Premium:** 10 € enkratno plačilo za neomejeno uporabo (prek Stripe)
- **Načrtovano:** e-mail tracking, analitika, B2B ponudbe, white-label možnost

---

## 🔐 Avtentikacija in nadzor dostopa

| Funkcija           | Brezplačno | Premium |
|--------------------|------------|---------|
| Pošiljanje emaila  | ✅ 1x       | ✅ neomejeno |
| Dostop do logov    | ✅         | ✅       |
| CSV izvoz logov    | ✅         | ✅       |
| Brisanje logov     | ✅         | ✅       |
| Dostop do predogleda emailov | ✅ | ✅       |

---

## 📦 Tehnične specifikacije

- **Backend:** Python (Flask)
- **Frontend:** HTML5, CSS3, Vanilla JS
- **Email:** `smtplib`, `email.message`
- **Avtentikacija:** Session-based (Flask sessions)
- **Plačila:** Stripe Checkout API
- **Baza podatkov:** SQLite + SQLAlchemy
- **Templating:** Jinja2
- **Okolje:** `.env` datoteka za varnost (API ključi, SMTP ...)
- **Zagon:** Localhost ali Railway (hostanje)

---

## 📊 SWOT analiza

| ✅ Prednosti             | ❌ Slabosti                        |
|--------------------------|------------------------------------|
| Hitra uporaba (plug & play) | Omejitve SMTP (brez lastne domene) |
| Enostaven UI/UX          | Potencialne zlorabe (phishing)    |
| Stripe integracija       | Brez e-mail verifikacije          |

| 🌱 Priložnosti           | ⚠️ Grožnje                         |
|--------------------------|------------------------------------|
| Razširitev na več podjetij | Konkurenca z večjimi orodji       |
| Komercialna uporaba (B2B) | Pravno vprašanje glede znamk      |

---

## ⚙️ Tehnične specifikacije

### 🔧 Backend
- **Flask** – mikro spletni framework za Python
- **Flask SQLAlchemy** – ORM za delo z SQLite bazo
- **Flask Sessions** – za sledenje prijavljenemu uporabniku (`session['user_id']`)
- **Stripe API** – integracija plačilnega sistema
- **SMTP (smtplib)** – za pošiljanje emailov
- **EmailMessage** – sestavljanje HTML sporočil
- **dotenv** – branje varnih podatkov iz `.env`

### 🧱 Baza podatkov
- **SQLite** – lokalna datoteka (`receiptgen.db`)
- **Tabele:**
  - `User`: uporabniški račun, geslo (hashed), premium status, uporabljen poskus
  - `EmailLog`: zgodovina poslanih emailov (timestamp, prejemnik, podjetje)

### 🎨 Frontend
- **HTML5/CSS3** – osnovna struktura in stil
- **Jinja2** – predloge za generiranje emailov (glede na izbrano podjetje)
- **JavaScript** – AJAX za predogled emaila pred pošiljanjem
- **Uporabniške strani:**
  - `index.html`: glavni obrazec za generacijo
  - `login.html`, `register.html`: avtentikacija
  - `logs.html`: pregled preteklih poslanih emailov
  - `pricing.html`: stran za nadgradnjo računa


## 📂 Zagon aplikacije (lokalno)

```bash
git clone https://github.com/tvoj-username/receiptgenerator.git
cd receiptgenerator
python -m venv venv
source venv/bin/activate   # ali venv\Scripts\activate na Windows
pip install -r requirements.txt
cp .env.example .env       # nastavi SMTP in Stripe ključe
python app.py
