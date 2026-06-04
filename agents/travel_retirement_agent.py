from core.agent_base import AgentBase
from tools.file_manager import FileManager
from tools.web_search import web_search
from tools.budget_calculator import BudgetCalculator
from tools.itinerary_generator import ItineraryGenerator
from tools.user_preferences import UserPreferences
from tools.tool_definitions import get_tool_definitions
from core.config import Config

class TravelRetirementAgent(AgentBase):
    def __init__(self):
        system_prompt = """You are an expert, warm, and highly capable Travel & Retirement Planning Agent for Australians.

        You have access to tools and remember user preferences.
        Be practical, empathetic, and well-organized."""
        
        super().__init__(system_prompt, get_tool_definitions())
        
        self.file_manager = FileManager(Config.PLANS_FOLDER)
        self.budget_calculator = BudgetCalculator()
        self.itinerary_generator = ItineraryGenerator()
        self.preferences = UserPreferences()
    
    def update_preference(self, key: str, value):
        self.preferences.update(key, value)
    
    def save_plan(self, title: str = None):
        if not title:
            title = "Travel_Retirement_Plan"
        filename = self.file_manager.save_conversation(title, self.messages)
        print(f"✅ Plan saved successfully: {filename}")
        return filename
    
    def export_markdown_plan(self, title: str = None):
        """Export current conversation as Markdown"""
        if not title:
            title = "Travel_Retirement_Plan"
        try:
            filename = self.file_manager.export_markdown(title, self.messages)
            return filename
        except Exception as e:
            print(f"❌ Failed to export Markdown: {e}")
            return None
           
    def show_preferences(self):
        """Display current user preferences"""
        prefs = self.preferences.preferences
        print("\n📋 Current User Preferences:")
        print("-" * 40)
        for key, value in prefs.items():
            print(f"• {key.replace('_', ' ').title()}: {value}")
        print("-" * 40)

    def export_markdown_plan(self, title: str = None):
        if not title:
            title = "Travel_Retirement_Plan"
        filename = self.file_manager.export_markdown(title, self.messages)
        return filename