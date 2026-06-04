import json
import os
from datetime import datetime

class UserPreferences:
    def __init__(self, filename="user_preferences.json"):
        self.filename = filename
        self.preferences = self._load_preferences()
    
    def _load_preferences(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return self._get_default_preferences()
        return self._get_default_preferences()
    
    def _get_default_preferences(self):
        return {
            "mobility": "standard",
            "budget_style": "comfortable",
            "interests": ["nature", "relaxation", "gentle walks"],
            "couple": True,
            "dietary": "none",
            "preferred_pace": "relaxed",
            "traveler_type": "Retiree Couple"
        }
    
    def update_preference(self, key: str, value):
        self.preferences[key] = value
        self._save_preferences()
    
    def get_preference(self, key: str):
        return self.preferences.get(key)
    
    def get_all(self):
        return self.preferences.copy()
    
    def _save_preferences(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.preferences, f, indent=2)
    
    def show_preferences(self):
        """Display preferences in Streamlit"""
        import streamlit as st
        st.subheader("📋 Current User Preferences")
        for key, value in self.preferences.items():
            nice_key = key.replace("_", " ").title()
            st.write(f"**{nice_key}:** {value}")