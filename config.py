import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    # AI Settings
    MODEL = "grok-4"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1200
    
    # Project settings
    PLANS_FOLDER = "travel_plans"
    DATA_FOLDER = "data"
    DEFAULT_CURRENCY = "AUD"
    
    # User defaults (you can change these)
    DEFAULT_LIFESTYLE = "comfortable"
    DEFAULT_TRAVELER_TYPE = "retiree_couple"
    
    # Export settings
    ENABLE_MARKDOWN_EXPORT = True