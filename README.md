# Underwriting MVP (Mock Mode)

A lightweight **digital underwriting system** built in **Python + Streamlit**, designed to demonstrate how a modern, paperless lending platform can collect applications, simulate soft credit pulls, and generate automated risk decisions.

---

## 🚀 Features

- **Digital Application Intake**
  - Collects applicant, business, and financial data
  - Includes consent, compliance, and community impact sections

- **Soft Pull Simulation**
  - Mimics a non-intrusive credit inquiry (Experian / TransUnion / Equifax mock)

- **Automated Scoring**
  - Calculates:
    - Debt Service Coverage Ratio (DSCR)
    - Underwriting Score (0–4 scale)
    - Risk Tier (A–D)
    - Decision Outcome (`approved`, `manual_review`, or `declined`)
  - Uses customizable logic from `scoring_logic.py`

- **Dashboard View**
  - Upload and score applications
  - Adjust inputs (credit, utilization, impact) dynamically
  - Instantly see changes in risk metrics and recommendations

---

## 🧠 Project Structure

```
underwriting_mvp/
│
├── app/                    # FastAPI service (optional backend)
├── data/                   # Saved applicant JSON files
├── streamlit_app.py        # Streamlit front-end dashboard
├── scoring_logic.py        # Core scoring algorithm
├── requirements.txt        # Dependencies
└── README.md               # You are here
```

---

## 🧮 How the Model Works

Each applicant’s data feeds into the scoring engine:
1. **Financial Health** → DSCR and revenue-to-debt ratio  
2. **Credit Behavior** → Soft pull simulation (credit band + utilization)  
3. **Operational Risk** → Years in business, compliance status  
4. **Community Impact** → Local job creation & economic effect  

Each factor contributes to a normalized underwriting score (0–4).  
The combined result determines the **Risk Tier** and **Decision Outcome**:

| Risk Tier | Range | Typical Decision | APR Estimate |
|------------|--------|------------------|---------------|
| A | 3.5–4.0 | Approved | 8–10% |
| B | 2.7–3.4 | Manual Review | 12–14% |
| C | 1.8–2.6 | Manual Review | 16–18% |
| D | <1.8 | Declined | N/A |

---

## ⚙️ Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/gantventures-wq/underwriting_mvp.git
   cd underwriting_mvp
   ```

2. Create virtual environment (Windows example):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch Streamlit dashboard:
   ```bash
   streamlit run streamlit_app.py
   ```

5. Visit the app at  
   👉 `http://localhost:8501`

---

## ☁️ Deploy to Streamlit Cloud

1. Push this project to GitHub  
2. Go to [https://share.streamlit.io](https://share.streamlit.io)  
3. Select:
   - Repo: `gantventures-wq/underwriting_mvp`
   - Branch: `main`
   - File path: `streamlit_app.py`

---

## 🧩 Future Enhancements
- Real credit bureau API integration (Experian, TransUnion, Equifax)
- Partner dashboard for underwriter reviews
- Machine learning risk model based on historic lending data
- Blockchain ledger for investor transparency (Crypto Capital integration)

---

## 🏗️ Built With
- **Python 3.11+**
- **Streamlit**
- **Pandas / Numpy**
- **FastAPI (optional backend)**

---

## 🧾 License
MIT License © 2025 Gant Ventures LLC
