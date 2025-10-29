# scoring_logic.py
from typing import Optional, Dict, Any

# ---- helpers ---------------------------------------------------------------

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(x, hi))

def tier_from_score(pct: float) -> str:
    if pct >= 85: return "A"
    if pct >= 70: return "B"
    if pct >= 55: return "C"
    if pct >= 40: return "D"
    return "F"

def apr_from_tier(base_prime: float = 8.5, tier: str = "B") -> float:
    """Legacy helper kept for reference (no longer used once dynamic APR is enabled)."""
    base = base_prime + 10.0
    adj = {"A": -2.0, "B": 0.0, "C": 2.0, "D": 4.0, "F": 0.0}.get(tier, 0.0)
    apr = base + adj
    return max(11.0, min(16.0, round(apr, 1)))

# ---- subscores -------------------------------------------------------------

def subscore_cashflow(dscr: Optional[float]) -> float:
    if dscr is None: return 0.0
    if dscr <= 1.00: return 0.0
    if dscr <= 1.25: return 1.0
    if dscr <= 1.75: return 2.0
    if dscr <= 2.50: return 3.0
    return 4.0

def subscore_ltv(loan_amount: float, collateral_value: Optional[float]) -> float:
    if collateral_value is None or collateral_value <= 0: return 0.0
    ltv = loan_amount / collateral_value
    if ltv > 1.00: return 0.0
    if ltv > 0.80: return 1.0
    if ltv > 0.60: return 2.0
    if ltv > 0.40: return 3.0
    return 4.0

def subscore_credit_band(band: Optional[str], utilization_pct: Optional[float]) -> float:
    band_map = {
        "poor":0, "fair":1, "good":2, "very good":3, "excellent":4,
        "580-599":0, "600-619":0, "620-639":1, "640-659":1, "660-679":2,
        "680-699":2, "700-719":3, "720-739":3, "740-759":4, "760-780":4
    }
    base = band_map.get((band or "").lower(), 2)
    if utilization_pct is None: return float(base)
    if utilization_pct > 50: base = max(0, base - 1)
    elif utilization_pct >= 40: base = max(0, base - 0.5)
    return float(base)

def subscore_competency(years: Optional[float]) -> float:
    if years is None: return 0.0
    if years < 1: return 0.0
    if years < 2: return 1.0
    if years < 4: return 2.0
    if years < 5: return 3.0
    return 4.0

def subscore_impact(impact_level: Optional[int]) -> float:
    if impact_level is None: return 2.0
    return float(max(0, min(4, impact_level)))

# ---- main ------------------------------------------------------------------

def score_application(app: Dict[str, Any], soft_pull: Optional[Dict[str, Any]]):
    # Inputs
    rev  = float(app.get("monthly_revenue", 0) or 0)
    exp  = float(app.get("monthly_expenses", 0) or 0)
    loan_amt = float(app.get("loan_amount_requested", 0) or 0)
    coll = float(app.get("collateral_value", 0) or 0)
    years = float(app.get("years_in_business", 0) or 0)

    # Cash flow & DSCR (simple mock payment)
    noi = max(0.0, rev - exp)
    est_payment = max(1.0, (loan_amt * 0.10) / 12.0)
    dscr = noi / est_payment

    # Soft pull (mock)
    band = util = None
    if soft_pull and soft_pull.get("ok"):
        band = soft_pull.get("score_band")
        util = soft_pull.get("utilization_pct")

    impact_level = app.get("impact_level")

    # Subscores (0–4)
    s_cash = subscore_cashflow(dscr)
    s_ltv  = subscore_ltv(loan_amt, coll)
    s_cred = subscore_credit_band(band or app.get("credit_score_band"), util)
    s_comp = subscore_competency(years)
    s_imp  = subscore_impact(impact_level)

    # Weighted composite (0–4)
    w_cash, w_cred, w_ltv, w_comp, w_imp = 0.35, 0.25, 0.20, 0.15, 0.05
    raw = (s_cash*w_cash + s_cred*w_cred + s_ltv*w_ltv + s_comp*w_comp + s_imp*w_imp)

    # Normalize to percent for tiering
    pct = round((raw / 4.0) * 100.0, 1)
    tier = tier_from_score(pct)
    decision = "auto_approve" if tier == "A" else ("manual_review" if tier in ("B", "C") else "decline")

    # ----------------- Dynamic APR (continuous) -----------------
    # Base APR goes 22% -> 8% as underwriting score goes 0.0 -> 4.0
    max_apr, min_apr = 22.0, 8.0
    base_apr = max_apr - (raw * 3.5)  # 4.0 => 8.0 ; 0.0 => 22.0

    # DSCR adjustments: reward strong cashflow, penalize weak
    dscr_adj = 0.0
    if dscr >= 2.0:      dscr_adj -= 1.2
    elif dscr >= 1.75:   dscr_adj -= 1.0
    elif dscr >= 1.25:   dscr_adj -= 0.5
    elif dscr < 1.10:    dscr_adj += 1.0

    # Utilization nudges APR up when high
    util_pct = (soft_pull or {}).get("utilization_pct")
    util_adj = (util_pct / 50.0) if isinstance(util_pct, (int, float)) else 0.0
    # e.g., 30% => +0.6 ; 80% => +1.6

    # Collateral (LTV) small discount for strong coverage
    ltv_adj = 0.0
    if coll and loan_amt > 0:
        ltv = loan_amt / coll
        if ltv <= 0.60:   ltv_adj -= 0.5
        elif ltv <= 0.80: ltv_adj -= 0.2

    apr = round(clamp(base_apr + dscr_adj + util_adj + ltv_adj, min_apr, max_apr), 1)
    # ----------------------------------------------------------------

    tranche = None
    if tier in ("C", "D"):
        tranche = "Stage funding (e.g., 50/50 or 30/30/40) + training/credit-repair."

    return {
        "dscr_estimate": round(dscr, 2),
        "subscores": {
            "cashflow": s_cash,
            "credit_util": s_cred,
            "collateral_ltv": s_ltv,
            "competency": s_comp,
            "community_impact": s_imp
        },
        "score_pct": pct,
        "risk_tier": tier,
        "decision": decision,
        "apr_estimate": apr,
        "tranche_guidance": tranche
    }
