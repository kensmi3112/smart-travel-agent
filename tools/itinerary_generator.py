from datetime import datetime

class ItineraryGenerator:
    def generate_itinerary(self, destination: str, duration_days: int, 
                         traveler_type: str = "retiree_couple", 
                         preferences: dict = None) -> str:
        """Generate structured itinerary based on traveler type"""
        
        if preferences is None:
            preferences = {}
        
        focus = preferences.get("focus", "relaxed")
        
        intro = f"**{duration_days}-Day {traveler_type.replace('_', ' ').title()} Itinerary for {destination}**\n"
        intro += f"**Focus:** {focus.title()}\n\n"
        
        # You can expand this with more traveler types later
        days = []
        for day in range(1, duration_days + 1):
            day_plan = f"**Day {day}: Relaxed Exploration**\nGentle activities with plenty of rest time."
            days.append(day_plan)
        
        tips = "\n**Practical Tips:**\n- Pace yourself\n- Book flexible activities\n- Check accessibility"
        
        return intro + "\n\n".join(days) + "\n\n" + tips