"""
handler for showing the main display
"""

APP_VERSION: str = "v0.1.0"

HELP_TEXT: str = f"""
 ______     __        ______   ______     __  __     ______     __  __     ______     ______  
/\  __ \   /\ \      /\  == \ /\  == \   /\ \/\ \   /\  ___\   /\ \_\ \   /\  __ \   /\__  _\ 
\ \  __ \  \ \ \     \ \  _-/ \ \  __<   \ \ \_\ \  \ \ \____  \ \  __ \  \ \  __ \  \/_/\ \/ 
 \ \_\ \_\  \ \_\     \ \_\    \ \_\ \_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\    \ \_\ 
  \/_/\/_/   \/_/      \/_/     \/_/ /_/   \/_____/   \/_____/   \/_/\/_/   \/_/\/_/     \/_/ 
                                                                                              
✨ AI PruChat, {APP_VERSION}. A modern command line application for ai assist ✨
"""

def show_help():
    return HELP_TEXT
