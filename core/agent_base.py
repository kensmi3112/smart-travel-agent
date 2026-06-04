import os
from abc import ABC
from openai import OpenAI
from core.config import Config

class AgentBase(ABC):
    """Robust base class with error handling and tool support"""
    
    def __init__(self, system_prompt: str, tools=None):
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.messages = [{"role": "system", "content": system_prompt}]
        self.available_tools = tools or []
        self.max_retries = 2
    
    def ask(self, question: str) -> str:
        self.messages.append({"role": "user", "content": question})
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=Config.MODEL,
                    messages=self.messages,
                    tools=self.available_tools,
                    tool_choice="auto",
                    temperature=Config.TEMPERATURE,
                    max_tokens=Config.MAX_TOKENS
                )
                
                message = response.choices[0].message
                self.messages.append(message)
                
                if not message.tool_calls:
                    return message.content
                
                # Tool handling (simplified for now)
                for tool_call in message.tool_calls:
                    result = self._execute_tool(tool_call)
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                
            except Exception as e:
                if attempt == self.max_retries:
                    return f"Apologies, I encountered an issue. Could you try again?"
                continue
                
        return "I'm having trouble right now."
    
    def _execute_tool(self, tool_call):
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"🔧 Tool called: {function_name}")
        
        if function_name == "web_search":
            from tools.web_search import web_search
            return web_search(arguments.get("query", ""))
        
        elif function_name == "budget_calculator":
            from tools.budget_calculator import BudgetCalculator
            calc = BudgetCalculator()
            result = calc.calculate_monthly_budget(
                location=arguments.get("location", ""),
                lifestyle=arguments.get("lifestyle", "comfortable"),
                couple=arguments.get("couple", True)
            )
            return calc.format_budget(result)
        
        return f"Tool {function_name} completed."