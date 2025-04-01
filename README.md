#  ReceiptGenerator

ReceiptGenerator je spletna aplikacija, ki omogoča uporabnikom pošiljanje realističnih potrditvenih e-poštnih sporočil iz različnih podjetij (npr. Apple, Amazon, Nike, StockX, GOAT ...). Uporabnik vnese potrebne podatke, izbere podjetje in aplikacija generira personaliziran email z izbranim dizajnom in ga pošlje na ciljni e-naslov.

---

##  Zakaj ReceiptGenerator?

###  Identifikacija problema

Veliko uporabnikov (npr. učenci, podjetniki, marketingaši) želi ustvariti realistične potrditve naročil za:
- testiranje,
- simulacije,
- predstavitve,
- šale.

Trenutno ni preproste spletne rešitve, ki omogoča prilagajanje email predlog in takojšnje pošiljanje. ReceiptGenerator to omogoča v nekaj sekundah.

### 🎯 Ciljna skupina
- Mladi med 14–25 let, ki želijo testirati spletno uporabniško izkušnjo
- Uporabniki, ki ustvarjajo demo vsebine
- Uporabniki z osnovnim znanjem spleta, ki želijo "fake receipt" generacijo brez programiranja

---

## 💡 Funkcionalnosti (MVP)

- ✅ Izbira podjetja (Apple, Amazon, Nike, StockX, GOAT ...)
- ✅ Vnos osnovnih podatkov (ime, naslov, izdelek, cena ...)
- ✅ Prilagajanje slike izdelka (URL)
- ✅ Samodejno generiranje email HTML-ja (Jinja2 templating)
- ✅ Pošiljanje emaila z SMTP (Gmail)
- ✅ Vizualno privlačne predloge

---

## 📊 Poslovni model

### Monetizacija (v prihodnosti):
- Premium: pošiljanje večih e-mailov/dan
- Statistika o odprtih e-mailih (tracking)
- "White label" verzija za podjetja
- Oglaševanje znotraj aplikacije

### Finančni plan:
- **Stroški:** gostovanje (Railway), domena, SMTP pošiljanje
- **Prihodki:** premium uporabniki, donacije, partnerstva

---

## 🔍 SWOT analiza

| ✅ Prednosti           | ❌ Slabosti                 |
|------------------------|----------------------------|
| Enostaven vmesnik      | Trenutno brez baze         |
| Razširljiv na več dizajnov | Brez preverjanja resničnosti podatkov |
| Jinja templating – preprosta razširitev | SMTP omejitve brez domene     |

| 🌱 Priložnosti         | ⚠️ Grožnje                  |
|------------------------|----------------------------|
| B2B uporaba (agencije) | Zloraba za phishing        |
| Možnost komercializacije | Tekmovanje z večjimi orodji |

---

## 🛠️ Tehnične specifikacije

- **Backend:** Flask (Python)
- **Email:** `smtplib`, `email.message`
- **Frontend:** HTML5, CSS3, Bootstrap (lahko dodaš)
- **Templating:** Jinja2
- **Okolje:** Railway / localhost
- **Datoteke okolja:** `.env`

---

