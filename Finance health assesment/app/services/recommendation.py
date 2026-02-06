from typing import Dict, Any
from app.models.company import Company

def analyze_company_health(company: Company, financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stub for LLM-based analysis.
    In real implementation, this would call GPT-5/Claude API.
    """
    
    # Mock analysis based on simple logical rules for now
    ratios = financial_data.get("ratios", {})
    margin = ratios.get("net_profit_margin", 0)
    
    score = 50.0
    risk = "medium"
    recommendations = []
    
    if margin > 0.20:
        score = 85.0
        risk = "low"
        recommendations.append("Healthy profit margins. Consider reinvesting in growth.")
    elif margin < 0.05:
        score = 40.0
        risk = "high"
        recommendations.append("Low profit margins. Review cost structure immediately.")
    else:
        score = 65.0
        risk = "medium"
        recommendations.append("Stable performance. Look for optimization opportunities.")
        
    return {
        "score": score,
        "risk_level": risk,
        "recommendations": recommendations,
        "narrative": "Based on the provided financial statements, the company shows..."
    }
