def get_tool_definitions():
    return [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for current information like weather, prices, news, visa rules, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "budget_calculator",
                "description": "Calculate monthly living or travel budget estimates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City or country"},
                        "lifestyle": {"type": "string", "enum": ["budget", "comfortable", "luxury"], "default": "comfortable"},
                        "couple": {"type": "boolean", "default": True}
                    },
                    "required": ["location"]
                }
            }
        }
    ]