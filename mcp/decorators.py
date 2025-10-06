from .registry import register_tool, register_resource, register_prompt

class MCP:
    def tool(self, name: str = None):
        def decorator(func):
            register_tool(name or func.__name__, func)
            return func
        return decorator

    def resource(self, name: str = None):
        def decorator(func):
            register_resource(name or func.__name__, func)
            return func
        return decorator

    def prompt(self, name: str = None):
        def decorator(func):
            register_prompt(name or func.__name__, func)
            return func
        return decorator

mcp = MCP()
