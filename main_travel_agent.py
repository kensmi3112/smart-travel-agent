from agents.travel_retirement_agent import TravelRetirementAgent

def main():
    print("=== 🌴 Smart Travel & Retirement Agent ===")
    print("Type any question or use these commands:")
    print("  • save plan [title]          → Save as text file")
    print("  • export markdown [title]    → Save as nice Markdown")
    print("  • quit / exit                → Exit\n")
    
    agent = TravelRetirementAgent()

    while True:
        q = input("\nYour question: ").strip()
        
        if q.lower() in ['quit', 'exit', 'q']:
            print("Happy planning! 👋")
            break
            
        if q.lower().startswith("save plan"):
            title = q[10:].strip() or "Travel Plan"
            agent.save_plan(title)
        
        elif q.lower().startswith("export markdown"):
            title = q[16:].strip() or "Travel Plan"
            agent.export_markdown_plan(title)
        
        elif q:
            answer = agent.ask(q)
            print(f"\n🌴 Agent Response:\n{answer}\n")

if __name__ == "__main__":
    main()