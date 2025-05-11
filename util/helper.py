"""
    Consists of helper functions
    & re-usable code snippets
"""
from typing import List, Dict

# show main menu options
# - Start a new chat
# - Add / Edit MCP servers
# - Access chat logs
# - Quit
def main_menu_options() -> List[str]:
    return ["1. Start a new chat", "2. Add / Remove MCP servers", "3. Access chat logs", "4. Quit"]


# convert tools into format required by bedrock
def convert_tool_format(tools) -> Dict:
    """
        Converts tools into format required by Bedrock API
        Args:
            tools (list): List of tool objects
        Returns:
            dict: tools in the format required by Bedrock API
    """
    converted_tools = []

    for tool in tools:
        tool_record = {
            "toolSpec": {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {
                    "json": tool.inputSchema
                }
            }
        }
        converted_tools.append(tool_record)
    # return desired format    
    return {"tools": converted_tools}
        
