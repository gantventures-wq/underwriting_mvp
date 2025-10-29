# 🏦 Underwriting Engine MVP

This is a working prototype of an automated underwriting engine built with FastAPI.  
It can intake loan applications, perform mock credit soft pulls, calculate underwriting scores, and return instant decisions.  
This system is structured so real credit bureau and payment integrations can be added later.

---

## ✨ Features
- 📥 Loan application intake
- 🪙 Mock credit bureau soft pull
- 📊 Automated DSCR & underwriting score calculation
- ⚡ Instant decision engine
- 🧰 Clean API interface with Swagger UI

---

## 🧭 Step-by-Step Instructions

### STEP 1 — 📦 Clone or Download the Project
- Unzip or clone the `underwriting-engine` folder to your computer.

---

### STEP 2 — 🐍 Create a Virtual Environment
```bash
python -m venv .venv
```

Activate it:

- **Windows:**
```bash
.\.venv\Scripts\activate
```

- **Mac / Linux:**
```bash
source .venv/bin/activate
```

You should now see `(.venv)` at the beginning of your terminal line.

---

### STEP 3 — 📥 Install Dependencies
Install all required Python packages using:

```bash
pip install -r requirements.txt
```

This ensures the environment matches exactly what was used to build the MVP.

---

### STEP 4 — 🚀 Run the API Server
Start the backend with:

```bash
uvicorn app.main:app --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

✅ That means the server is live.

---

### STEP 5 — 🌐 Open Swagger UI
In your browser, go to:

```
http://127.0.0.1:8000/docs
```

Swagger UI is your control panel for testing the API.

---

### STEP 6 — 🧪 Run a Full Underwriting Demo

#### 1️⃣ Create an Application
- Select `POST /applications` in Swagger.
- Click **Try it out** → **Execute**.
- This will return an `app_id`.

#### 2️⃣ Mock Credit Pull
- Select `POST /applications/{app_id}/soft-pull`.
- Paste your `app_id` in the parameter box.
- Click **Execute**.
- You’ll see a mock credit score & utilization.

#### 3️⃣ Underwriting Score & Decision
- Select `POST /applications/{app_id}/score`.
- Paste the same `app_id`.
- Click **Execute**.
- The system will return a decision such as:
```json
{
  "app_id": "app-12345",
  "approved": true,
  "score": 720,
  "risk_tier": "A",
  "dscr": 1.35
}
```

🎯 Boom — full loan decision flow in seconds.

---

### STEP 7 — 🧰 Optional Commands

- **Deactivate virtual environment:**
```bash
deactivate
```

- **Reinstall dependencies if needed:**
```bash
pip install -r requirements.txt
```

---

## 📈 Future Enhancements
- Real credit bureau integration (Experian / TransUnion / Equifax)
- ACH payment processing
- Admin dashboard with borrower pipeline
- Authentication & compliance modules

---

## 👤 Author
Created by **Gant Ventures LLC**  
All Rights Reserved.  
For partnership or licensing inquiries, contact gantventures@gmail.com
