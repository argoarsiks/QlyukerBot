import os
from rich.console import Console
from rich.table import Table
from rich.box import DOUBLE


def consoleInfo(currentEnergy, currentCoins, currentTickets, minePerHour):
    os.system("cls" if os.name == "nt" else "clear")

    console = Console()

    table = Table(title="Stats", show_header=True, header_style="bold magenta", box=DOUBLE, expand=True, width=console.width)
    table.add_column("Param", style="blue")
    table.add_column("Value", style="green")
    
    table.add_row("Coins", str(currentCoins))
    table.add_row("Energy", str(currentEnergy))
    table.add_row("Tickets", str(currentTickets))
    table.add_row("Coins/hour", f"{minePerHour}/h")
    table.add_row("Tickets/hour", f"{minePerHour / 10000:.2f}/h")
    
    console.print(table)