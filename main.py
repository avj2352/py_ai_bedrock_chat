import typer
from simple_term_menu import TerminalMenu
from rich.console import Console
# ..handlers
from handlers.about import show_help
from handlers.chat import init_agent_chat
# ..custom
from util.helper import main_menu_options

console = Console()
app = typer.Typer()


# main entry
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Main CLI application"""
    text = show_help()
    console.print(text)
    # show main menu options
    options = main_menu_options()
    terminal_menu = TerminalMenu(options, title="Select an option:")
    choice_index = terminal_menu.show()
    # handle user choice
    if choice_index is None:
        raise typer.Exit()

    # if option == 4. Quit
    elif choice_index is not None and options[choice_index] == main_menu_options()[3]:
        raise typer.Exit()    
    # if option == 1. Start a new chat
    elif choice_index is not None and options[choice_index] == main_menu_options()[0]:
        init_agent_chat()
    else:
        typer.echo(f"You selected: {options[choice_index]}")

# init app
if __name__ == "__main__":
    app()
