"""
Simple Memory Manager for EcoVibe Concierge
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

class MemoryManager:
    def __init__(self, memory_dir="memory"):
        self.memory_dir = memory_dir
        self.user_profile_path = os.path.join(memory_dir, "user_profile.json")
        os.makedirs(memory_dir, exist_ok=True)
        self.load_profile()

    def load_profile(self) -> Dict:
        """Load user profile from JSON"""
        if os.path.exists(self.user_profile_path):
            with open(self.user_profile_path, 'r') as f:
                self.profile = json.load(f)
        else:
            self.profile = {
                "user_id": "default_user",
                "name": "User",
                "location": "Unknown",
                "preferences": {},
                "stats": {},
                "last_updated": datetime.now().isoformat()
            }
            self.save_profile()
        return self.profile

    def save_profile(self):
        """Save user profile to JSON"""
        with open(self.user_profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)

    def update_stat(self, key: str, value: Any):
        """Update a statistic"""
        self.profile["stats"][key] = value
        self.profile["last_updated"] = datetime.now().isoformat()
        self.save_profile()

    def get_profile(self) -> Dict:
        """Return current user profile"""
        return self.profile

# Simple test
if __name__ == "__main__":
    memory = MemoryManager()
    print("User Profile Loaded:")
    print(json.dumps(memory.get_profile(), indent=2))