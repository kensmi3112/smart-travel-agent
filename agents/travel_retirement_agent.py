from core.agent_base import AgentBase
from tools.file_manager import FileManager
from tools.budget_calculator import BudgetCalculator
from tools.itinerary_generator import ItineraryGenerator
from tools.tool_definitions import get_tool_definitions
from core.config import Config


class TravelRetirementAgent(AgentBase):
    def __init__(self):
        system_prompt = """You are an expert, warm, and highly capable Travel Planning Agent.

You have access to tools and remember user preferences.
Be practical, empathetic, and well-organized."""
        
        super().__init__(system_prompt, get_tool_definitions())
        
        self.file_manager = FileManager(Config.PLANS_FOLDER)
        self.budget_calculator = BudgetCalculator()
        self.itinerary_generator = ItineraryGenerator()
        
        # Simple preferences dictionary to avoid circular import
        self.preferences = {"location": "Australia", "currency": "AUD"}
    
    def update_preference(self, key: str, value):
        """Update user preference"""
        self.preferences[key] = value
        print(f"✅ Preference updated: {key} = {value}")
    
    def save_plan(self, title: str = None):
        if not title:
            title = "Travel_Plan"
        filename = self.file_manager.save_conversation(title, self.messages)
        print(f"✅ Plan saved successfully: {filename}")
        return filename
    
    def export_markdown_plan(self, title: str = None):
        if not title:
            title = "Travel_Plan"
        try:
            filename = self.file_manager.export_markdown(title, self.messages)
            return filename
        except Exception as e:
            print(f"❌ Failed to export: {e}")
            return None