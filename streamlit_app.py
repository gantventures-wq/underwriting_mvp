# streamlit_app.py
import os, json, datetime
import streamlit as st
from scoring_logic import score_application

st.set_page_config(page_title="Underwriting Intake & Dashboard", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def app_id_now():
    return "app-" + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

st.title("Underwriting – Applicant Intake & Scoring (Mock Mode)")

tab1, tab2 = st.tabs(["📝 Applicant Intake", "📊 Underwriting Dashboard"])

with tab1:
    st.subheader("Applicant Intake Form")
    with st.form("intake_form", clear_on_submit=False):
        # Identity
        c1, c2, c3 = st.columns(3)
        first = c1.text_input("First name")
        last  = c2.text_input("Last name")
        email = c3.text_input("Email")

        c1, c2 = st.columns(2)
        phone = c1.text_input("Phone")
        home_addr = c2.text_input("Home address (street, city, state, ZIP)")

        # Business profile
        st.markdown("### Business Profile")
        c1, c2 = st.columns(2)
        biz_name = c1.text_input("Legal business name")
        ein = c2.text_input("EIN (Tax ID)", placeholder="12-3456789")
        biz_addr = st.text_input("Business address (street, city, state, ZIP)")
        biz_type = st.selectbox("Business type/industry", [
            "Logistics & Transportation","Retail","Food Service","Marketing & Advertising",
            "Construction","Professional Services","Health & Beauty","Manufacturing","Other"
        ])
        entity = st.selectbox("Entity type", ["LLC","S-Corp","C-Corp","Sole Prop","Non-profit"])
        years_in_business = st.number_input("Years in business", min_value=0.0, step=0.5)

        # Loan & use
        st.markdown("### Loan Purpose")
        c1, c2, c3 = st.columns(3)
        loan_amount = c1.number_input("Loan amount requested", min_value=0.0, step=1000.0)
        term_months = c2.number_input("Desired term (months)", min_value=3, step=3, value=12)
        loan_purpose = c3.selectbox("Use of funds", ["Working capital","Equipment","Inventory","Marketing","Refinance","Other"])

        # Financials
        st.markdown("### Revenues & Expenses")
        c1, c2, c3 = st.columns(3)
        monthly_rev = c1.number_input("Avg monthly revenue", min_value=0.0, step=100.0)
        monthly_exp = c2.number_input("Avg monthly expenses", min_value=0.0, step=100.0)
        existing_debt = c3.number_input("Existing monthly debt payments (optional)", min_value=0.0, step=50.0)

        # Collateral
        st.markdown("### Collateral (optional)")
        c1, c2 = st.columns(2)
        collateral_type = c1.selectbox("Collateral type", ["None","Vehicle/Equipment","Accounts Receivable","Other"])
        collateral_value = c2.number_input("Estimated collateral value", min_value=0.0, step=500.0)

        # Credit (mock) & consent
        st.markdown("### Credit (Mock Soft Pull)")
        c1, c2, c3 = st.columns(3)
        credit_band = c1.selectbox("Estimated credit band", [
            "580-599","600-619","620-639","640-659","660-679","680-699","700-719","720-739","740-759","760-780"
        ], index=6)
        utilization_pct = c2.slider("Credit utilization %", 0, 100, 35)
        soft_pull_consent = c3.checkbox("I consent to a soft credit pull (mock)")

        # Compliance (mock)
        st.markdown("### Compliance Checklist (mock)")
        c1, c2, c3, c4 = st.columns(4)
        has_articles = c1.checkbox("Articles of Organization")
        good_standing = c2.checkbox("Certificate of Good Standing")
        has_license = c3.checkbox("Business license(s) current")
        has_insurance = c4.checkbox("Liability insurance active")

        # References (optional)
        st.markdown("### References (optional)")
        r1_name = st.text_input("Reference #1 name", "")
        r1_rel  = st.text_input("Reference #1 relationship", "")
        r1_phone= st.text_input("Reference #1 phone", "")
        r2_name = st.text_input("Reference #2 name", "")
        r2_rel  = st.text_input("Reference #2 relationship", "")
        r2_phone= st.text_input("Reference #2 phone", "")

       # Impact
        st.markdown("### Community Impact (demo)")
        ci1, ci2 = st.columns([1, 3])

        # Applicant enters estimated jobs
        jobs = ci1.number_input(
    "Estimated jobs created/retained",
        min_value=0,
        step=1,
        value=0
)

        # Applicant selects impact level (with help tooltip)
        impact_level = ci2.slider(
    "Community Impact (0–4)",
    0, 4, 2,
        help=(
        "Use this scale to rate your business's local impact:\n\n"
        "0 – No measurable community impact\n"
        "1 – Small impact (e.g., serves locals but no jobs created yet)\n"
        "2 – Moderate impact (a few jobs or local contracts)\n"
        "3 – Strong impact (multiple local employees, partnerships)\n"
        "4 – Major impact (job creation, increased tax revenue, anchors other businesses)"
    )
)

        # Attestations
        st.markdown("### Verifications")
        attest_true = st.checkbox("I certify the information is true and accurate.")
        attest_auth = st.checkbox("I authorize evaluation for financing.")

        submitted = st.form_submit_button("Save & Score")
        if submitted:
            if not (first and last and email and biz_name and attest_true and attest_auth):
                st.error("Please fill the basic required fields and attest.")
            else:
                app_id = app_id_now()
                app = {
                    "application_id": app_id,
                    "applicant": {
                        "first_name": first, "last_name": last, "email": email, "phone": phone,
                        "address": home_addr
                    },
                    "business_name": biz_name,
                    "business_address": biz_addr,
                    "business_type": biz_type,
                    "entity_type": entity,
                    "business_ein": ein,
                    "years_in_business": years_in_business,
                    "loan_amount_requested": loan_amount,
                    "loan_term_months": term_months,
                    "loan_purpose": loan_purpose,
                    "monthly_revenue": monthly_rev,
                    "monthly_expenses": monthly_exp,
                    "existing_debt_monthly_payment": existing_debt,
                    "collateral_type": collateral_type,
                    "collateral_value": collateral_value,
                    "credit_score_band": credit_band,
                    "impact_level": impact_level,
                    "jobs_estimate": jobs,
                    "compliance": {
                        "has_articles": has_articles,
                        "good_standing": good_standing,
                        "has_license": has_license,
                        "has_insurance": has_insurance
                    },
                    "consents": {
                        "soft_pull_consent": soft_pull_consent
                    },
                    "references": [
                        {"name": r1_name, "relationship": r1_rel, "phone": r1_phone} if r1_name else None,
                        {"name": r2_name, "relationship": r2_rel, "phone": r2_phone} if r2_name else None
                    ],
                    "metadata": {
                        "submitted_at": datetime.datetime.utcnow().isoformat() + "Z",
                        "channel": "streamlit-intake",
                        "status": "pending"
                    }
                }
                app["references"] = [r for r in app["references"] if r]

                # save JSON
                out_path = os.path.join(DATA_DIR, f"{app_id}.json")
                save_json(app, out_path)
                st.success(f"Saved application as {out_path}")

                # soft pull (mock)
                soft_pull = {"ok": True, "score_band": credit_band, "utilization_pct": utilization_pct}
                res = score_application(app, soft_pull)

                st.subheader("Decision Summary")
                colA, colB, colC, colD, colE = st.columns(5)
                colA.metric("Decision", res["decision"])
                colB.metric("Risk Tier", res["risk_tier"])
                colC.metric("APR Estimate", f'{res["apr_estimate"]}%')
                colD.metric("DSCR (est.)", res["dscr_estimate"])
                colE.metric("Score (%)", res["score_pct"])
                st.write("Subscores (0–4):", res["subscores"])
                if res.get("tranche_guidance"):
                    st.info(res["tranche_guidance"])

with tab2:
    st.subheader("Score Existing Applications")
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    pick = st.selectbox("Choose an application in /data", files) if files else None

    uploaded = st.file_uploader("…or upload a JSON file", type=["json"])
    app = None
    if uploaded:
        app = json.loads(uploaded.read().decode("utf-8"))
    elif pick:
        app = load_json(os.path.join(DATA_DIR, pick))

    st.markdown("### Credit & Impact Overrides (mock)")
    col1, col2, col3 = st.columns(3)
    band = col1.selectbox("Credit band", [
        "580-599","600-619","620-639","640-659","660-679","680-699","700-719","720-739","740-759","760-780"
    ], index=6)
    util = col2.slider("Utilization %", 0, 100, 35)
    impact = col3.slider("Community Impact (0–4)", 0, 4, 2)

    if app:
        app["impact_level"] = impact
        soft_pull = {"ok": True, "score_band": band, "utilization_pct": util}
        res = score_application(app, soft_pull)

        st.subheader("Decision Summary")
        colA, colB, colC, colD, colE = st.columns(5)
        colA.metric("Decision", res["decision"])
        colB.metric("Risk Tier", res["risk_tier"])
        colC.metric("APR Estimate", f'{res["apr_estimate"]}%')
        colD.metric("DSCR (est.)", res["dscr_estimate"])
        colE.metric("Score (%)", res["score_pct"])
        st.write("Subscores (0–4):", res["subscores"])
        if res.get("tranche_guidance"):
            st.info(res["tranche_guidance"])
        st.caption("Loaded application JSON:")
        st.json(app)
    else:
        st.warning("Select or upload an application JSON.")
