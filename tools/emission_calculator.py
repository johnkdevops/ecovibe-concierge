"""
Emission Calculator Tool for EcoVibe Concierge
Used by the Tracker Agent
"""

from typing import Dict, List, Tuple
import json

class EmissionCalculator:
    """
    Calculates carbon emissions for various activities and provides recommendations.
    """
    
    # Emission factors (kg CO2e per unit) - grounded in reliable sources
    EMISSION_FACTORS = {
        "driving": {
            "miles": 0.404,      # Average gasoline car (US)
            "km": 0.251
        },
        "flying": {
            "miles": 0.235,      # Economy class
            "km": 0.146
        },
        "beef": {
            "kg": 99.48,         # Per kg of beef
            "meal": 15.0         # Average beef meal
        },
        "electricity": {
            "kwh": 0.385         # US average grid
        },
        "public_transport": {
            "miles": 0.089,      # Bus
            "km": 0.055
        }
    }

    def calculate_emissions(self, activity: str, value: float, unit: str = "miles") -> Dict:
        """
        Calculate CO2e emissions for an activity.
        
        Args:
            activity: Type of activity (driving, flying, beef, etc.)
            value: Quantity (distance, kg, kwh, etc.)
            unit: Unit of measurement
            
        Returns:
            Dictionary with emissions data
        """
        if activity not in self.EMISSION_FACTORS:
            return {
                "activity": activity,
                "emissions_kg": 0.0,
                "confidence": 0.0,
                "error": f"Unknown activity: {activity}"
            }
        
        factor_key = unit if unit in self.EMISSION_FACTORS[activity] else list(self.EMISSION_FACTORS[activity].keys())[0]
        factor = self.EMISSION_FACTORS[activity].get(factor_key, 0.0)
        
        emissions = value * factor
        
        return {
            "activity": activity,
            "value": value,
            "unit": unit,
            "emissions_kg": round(emissions, 2),
            "confidence": 0.85,
            "source": "EPA & DEFRA average factors (2025)"
        }

    def get_recommendations(self, activity: str, value: float, unit: str = "miles") -> List[Dict]:
        """
        Get practical recommendations to reduce emissions for this activity.
        """
        recommendations = []
        
        if activity == "driving":
            recommendations = [
                {"action": "Switch to public transport", "potential_savings_kg": round(value * 0.3, 1), "difficulty": "medium"},
                {"action": "Carpool or ride-share", "potential_savings_kg": round(value * 0.5, 1), "difficulty": "easy"},
                {"action": "Use an electric vehicle", "potential_savings_kg": round(value * 0.85, 1), "difficulty": "high"}
            ]
        elif activity == "beef":
            recommendations = [
                {"action": "Replace with plant-based alternative", "potential_savings_kg": round(value * 0.9, 1), "difficulty": "medium"},
                {"action": "Reduce portion size", "potential_savings_kg": round(value * 0.4, 1), "difficulty": "easy"}
            ]
        
        return recommendations[:3]  # Limit to top 3

    def get_weekly_summary(self, activities: List[Dict]) -> Dict:
        """Generate a weekly summary from multiple activities."""
        total = sum(a.get("emissions_kg", 0) for a in activities)
        
        return {
            "total_emissions_kg": round(total, 2),
            "activities_count": len(activities),
            "average_daily_kg": round(total / 7, 2) if activities else 0,
            "status": "Good" if total < 50 else "Needs Attention"
        }


# Simple test when run directly
if __name__ == "__main__":
    calculator = EmissionCalculator()
    
    result = calculator.calculate_emissions("driving", 100, "miles")
    print("Emission Calculation:", result)
    
    recs = calculator.get_recommendations("driving", 100, "miles")
    print("Recommendations:", recs)