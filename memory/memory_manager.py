"""
EcoVibe Concierge - Long-Term Context & State Persistence Subsystem
Manages user profiles, habits, carbon budgets, and historical goal milestones.
"""

import os
import json
from threading import Lock

PROFILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "memory",
    "user_profile.json"
)

# Thread-safety lock for multi-threaded FastAPI environments
_profile_lock = Lock()

class MemoryManager:
    @staticmethod
    def get_default_profile() -> dict:
        return {
            "user_id": "default_eco_user",
            "name": "Eco Explorer",
            "habits": {
                "preferred_transit": "public",
                "dietary_preference": "vegetarian-curious",
                "home_energy": "electric"
            },
            "active_goals": [
                "Reduce gasoline driving by 20% this month",
                "Log at least 3 low-carbon diet decisions weekly"
            ],
            "historic_footprint_kg": 134.82,
            "completed_actions": []
        }

    @classmethod
    def load_profile(cls) -> dict:
        """Loads user profile from memory cache safely."""
        with _profile_lock:
            if not os.path.exists(PROFILE_PATH):
                os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
                cls.save_profile(cls.get_default_profile())
                return cls.get_default_profile()
            
            try:
                with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return cls.get_default_profile()

    @classmethod
    def save_profile(cls, profile_data: dict) -> bool:
        """Saves user profile safely."""
        with _profile_lock:
            try:
                os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
                with open(PROFILE_PATH, "w", encoding="utf-8") as f:
                    json.dump(profile_data, f, indent=4, ensure_ascii=False)
                return True
            except Exception:
                return False

    @classmethod
    def update_habits(cls, new_habits: dict) -> dict:
        """Updates specific user habits inside the state ledger."""
        profile = cls.load_profile()
        profile["habits"].update(new_habits)
        cls.save_profile(profile)
        return profile

    @classmethod
    def add_footprint_metric(cls, emissions_kg: float):
        """Appends emitted CO2 quantities to historical totals."""
        profile = cls.load_profile()
        profile["historic_footprint_kg"] = round(profile.get("historic_footprint_kg", 0.0) + emissions_kg, 2)
        cls.save_profile(profile)