import json
import os
from core.config import Config

class BudgetCalculator:
    def __init__(self):
        self.currency = Config.DEFAULT_CURRENCY
        self.cost_data = self._load_cost_data()
    
    def _load_cost_data(self):
        try:
            path = "data/location_costs.json"
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cost data: {e}")
            return {"locations": {}, "adjustment_factors": {}}
    
    def calculate_monthly_budget(self, location: str, lifestyle: str = "comfortable", couple: bool = True, custom_multiplier: float = 1.0) -> dict:
        location = location.strip().title()
        
        costs = self.cost_data["locations"].get(location)
        if not costs:
            costs = self.cost_data["locations"].get("Shepparton", {"comfortable": 4000})
        
        base = costs.get(lifestyle.lower(), costs.get("comfortable", 4000))
        
        # Apply adjustments
        if not couple:
            base = int(base * self.cost_data.get("adjustment_factors", {}).get("single", 0.65))
        
        base = int(base * custom_multiplier)
        
        breakdown = {
            "Housing": int(base * 0.42),
            "Food & Groceries": int(base * 0.18),
            "Transport": int(base * 0.08),
            "Healthcare & Insurance": int(base * 0.12),
            "Leisure & Activities": int(base * 0.10),
            "Utilities & Internet": int(base * 0.07),
            "Miscellaneous": int(base * 0.03),
        }
        
        return {
            "location": location,
            "lifestyle": lifestyle,
            "couple": couple,
            "total_monthly": base,
            "breakdown": breakdown,
            "currency": self.currency,
            "note": f"Estimates in {self.currency}. Adjust with web search for latest prices."
        }
    
    def format_budget(self, budget_data: dict) -> str:
        lines = [f"**Monthly Budget for {budget_data['location']}**"]
        lines.append(f"**Lifestyle:** {budget_data['lifestyle'].capitalize()} | **For:** {'Couple' if budget_data['couple'] else 'Single'}")
        lines.append(f"**Total:** ${budget_data['total_monthly']:,} {budget_data['currency']}\n")
        
        lines.append("| Category                    | Monthly Cost |")
        lines.append("|-----------------------------|--------------|")
        for cat, amount in budget_data["breakdown"].items():
            lines.append(f"| {cat:<27} | ${amount:>10,} |")
        
        lines.append(f"\n*{budget_data['note']}*")
        return "\n".join(lines)