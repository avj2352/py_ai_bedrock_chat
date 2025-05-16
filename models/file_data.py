"""
    File data model for
    'config.json'
    Includes the following fields
    - mcp
    - agent
"""
from dataclasses import dataclass
from typing import List

# default agent list (prepopulate)
default_agents: List[str] = [
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-7-sonnet-20250219-v1:0",
    "amazon.nova-sonic-v1:0"
]

# mcp field structure
@dataclass(kw_only=True)
class Mcp:
    name: str
    description: str
    server: str
    type: str = "sse"

    # validation
    def __post_init__(self):
        if self.type not in ['sse', 'stdio', 'http']:
            raise ValueError("invalid type")

# filedata structure
@dataclass(kw_only=True)
class FileData:
    mcp: List[Mcp] = []
    agents: List[str] = default_agents
