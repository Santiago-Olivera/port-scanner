from colorama import Fore, Style, init

# Initialize colorama for Windows support
init()

def print_status(message, status="info"):
    """Prints a status message in color."""
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED
    }
    print(colors.get(status, Fore.WHITE) + message + Style.RESET_ALL)
