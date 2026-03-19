from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class FiveCsScore:
    character: float
    capacity: float
    capital: float
    collateral: float
    conditions: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


def compute_risk_score(financials: Dict[str, Any], research: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple, explainable risk scoring model based on Five Cs of Credit.
    Score range: 0–100
    """
    revenue = float(financials.get("revenue") or 0.0)
    profit = float(financials.get("profit") or 0.0)
    debt = float(financials.get("debt") or 0.0)
    assets = float(financials.get("assets") or 0.0)
    cash_flow = float(financials.get("cash_flow") or 0.0)

    litigation_cases = int(research.get("litigation_cases") or 0)
    promoter_reputation = str(research.get("promoter_reputation") or "average")
    sector_outlook = str(research.get("sector_outlook") or "stable")
    sentiment_score = float(research.get("sentiment_score") or 0.0)

    score = 50.0
    explanations: list[str] = []

    # Capacity – cash flows vs debt
    if debt > 0 and cash_flow > 0:
        coverage = cash_flow / (debt / 5 or 1)  # rough proxy
        if coverage > 1.5:
            score += 10
            explanations.append("Strong cash flow coverage relative to debt (Capacity +10).")
        elif coverage > 1.0:
            score += 5
            explanations.append("Adequate cash flow coverage relative to debt (Capacity +5).")
        else:
            score -= 10
            explanations.append("Weak cash flow coverage relative to debt (Capacity -10).")

    # Capital – leverage and profitability
    if assets > 0 and debt > 0:
        leverage = debt / assets
        if leverage < 0.4:
            score += 8
            explanations.append("Low leverage relative to assets (Capital +8).")
        elif leverage < 0.7:
            score += 4
            explanations.append("Moderate leverage (Capital +4).")
        else:
            score -= 8
            explanations.append("High leverage relative to assets (Capital -8).")

    if profit <= 0:
        score -= 12
        explanations.append("Loss-making or low profitability (Capital -12).")
    elif profit / (revenue or 1) > 0.1:
        score += 6
        explanations.append("Healthy profit margin (Capital +6).")

    # Character – promoter reputation, litigation, sentiment
    if promoter_reputation == "strong":
        score += 6
        explanations.append("Strong promoter reputation (Character +6).")
    elif promoter_reputation == "weak":
        score -= 8
        explanations.append("Weak promoter reputation (Character -8).")

    if litigation_cases == 1:
        score -= 8
        explanations.append("Single litigation case identified (Character -8).")
    elif litigation_cases >= 2:
        score -= 16
        explanations.append("Multiple litigation cases identified (Character -16).")

    if sentiment_score > 0.3:
        score += 4
        explanations.append("Positive news sentiment (Character +4).")
    elif sentiment_score < -0.3:
        score -= 4
        explanations.append("Negative news sentiment (Character -4).")

    # Collateral – proxied by asset base vs debt
    if assets and debt:
        if assets > 2.5 * debt:
            score += 10
            explanations.append("Strong asset cover over debt (Collateral +10).")
        elif assets > 1.5 * debt:
            score += 5
            explanations.append("Adequate asset cover (Collateral +5).")
        else:
            score -= 5
            explanations.append("Limited asset cover (Collateral -5).")

    # Conditions – sector outlook
    if sector_outlook in {"high growth", "moderate growth"}:
        score += 6
        explanations.append("Favorable sector outlook (Conditions +6).")
    elif sector_outlook == "under stress":
        score -= 10
        explanations.append("Sector currently under stress (Conditions -10).")

    # Clamp score
    score = max(0.0, min(100.0, score))

    if score >= 75:
        risk_level = "Low"
    elif score >= 55:
        risk_level = "Medium"
    else:
        risk_level = "High"

    five_cs = FiveCsScore(
        character=max(0.0, min(100.0, 50 + (10 if promoter_reputation == "strong" else -5 * litigation_cases))),
        capacity=max(0.0, min(100.0, 50 + (10 if cash_flow > debt / 5 else -10))),
        capital=max(0.0, min(100.0, 50 + (10 if profit > 0 else -10))),
        collateral=max(0.0, min(100.0, 50 + (10 if assets > debt else -5))),
        conditions=max(0.0, min(100.0, 50 + (10 if sector_outlook in {"high growth", "moderate growth"} else -10))),
    )

    return {
        "risk_score": round(score, 2),
        "risk_level": risk_level,
        "five_cs": five_cs.to_dict(),
        "explanations": explanations,
    }

