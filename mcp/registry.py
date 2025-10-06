TOOLS = {}
RESOURCES = {}
PROMPTS = {}

def register_tool(name: str, func):
    TOOLS[name] = func

def register_resource(name: str, func):
    RESOURCES[name] = func

def register_prompt(name: str, func):
    PROMPTS[name] = func
