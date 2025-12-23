# project.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich import box
import math
import json
import os

console = Console()

# File to save conversion history
HISTORY_FILE = "conversion_history.json"


def load_history():
    """Load conversion history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(entry):
    """Save a new conversion to history (keeps only last 20 entries)"""
    history = load_history()
    history.append(entry)
    history = history[-20:]  # Keep only the latest 20
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def is_prime(n):
    """Check if a number is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def solve_quadratic(a, b, c):
    """Solve quadratic equation ax² + bx + c = 0 and return roots description"""
    discriminant = b**2 - 4 * a * c

    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"Two distinct real roots: {root1:.6f} and {root2:.6f}"
    elif discriminant == 0:
        root = -b / (2 * a)
        return f"One real root (repeated): {root:.6f}"
    else:
        real_part = -b / (2 * a)
        imag_part = math.sqrt(-discriminant) / (2 * a)
        return f"Two complex roots: {real_part:.6f} ± {imag_part:.6f}i"


# Unit conversion data
conversions = {
    "Length": {
        "meter": 1,
        "kilometer": 1000,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "mile": 1609.34,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254,
    },
    "Weight": {
        "kilogram": 1,
        "gram": 0.001,
        "ton": 1000,
        "pound": 0.453592,
        "ounce": 0.0283495,
    },
    "Temperature": {
        "Celsius": "celsius",
        "Fahrenheit": "fahrenheit",
        "Kelvin": "kelvin",
    }
}


def convert_temperature(value, from_unit, to_unit):
    """Convert between Celsius, Fahrenheit, and Kelvin"""
    # First convert to Celsius
    if from_unit == "Fahrenheit":
        c = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        c = value - 273.15
    else:  # Celsius
        c = value

    # Then convert from Celsius to target
    if to_unit == "Fahrenheit":
        return c * 9 / 5 + 32
    elif to_unit == "Kelvin":
        return c + 273.15
    else:  # Celsius
        return c


def convert_unit(value, category, from_unit, to_unit):
    """Perform unit conversion based on category"""
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)

    factor_from = conversions[category][from_unit]
    factor_to = conversions[category][to_unit]
    return value * factor_from / factor_to


def main():
    history = load_history()

    console.print(
        Panel.fit(
            "[bold magenta]🛠 Smart Unit Converter + Prime Checker + Quadratic Solver[/bold magenta]",
            box=box.DOUBLE,
        )
    )

    while True:
        console.print("\n[bold cyan]Main Menu:[/bold cyan]")
        console.print("1. Unit Conversion")
        console.print("2. Prime Number Checker")
        console.print("3. Quadratic Equation Solver")
        console.print("4. View Conversion History")
        console.print("5. Exit")

        choice = Prompt.ask(
            "\nSelect an option",
            choices=["1", "2", "3", "4", "5"],
            default="1",
        )

        if choice == "1":
            console.print("\n[bold yellow]Categories:[/bold yellow]")
            categories = list(conversions.keys())
            for i, cat in enumerate(categories, 1):
                console.print(f"{i}. {cat}")

            cat_idx = IntPrompt.ask(
                "Choose category",
                choices=[str(i) for i in range(1, len(categories) + 1)],
            )
            category = categories[cat_idx - 1]

            units = list(conversions[category].keys())
            table = Table(title=f"{category} Units", box=box.ROUNDED)
            table.add_column("No.", style="cyan")
            table.add_column("Unit", style="magenta")
            for i, unit in enumerate(units, 1):
                table.add_row(str(i), unit)
            console.print(table)

            value = FloatPrompt.ask(f"\nEnter value")

            from_idx = (
                IntPrompt.ask(
                    "From unit (number)",
                    choices=[str(i) for i in range(1, len(units) + 1)],
                )
                - 1
            )
            to_idx = (
                IntPrompt.ask(
                    "To unit (number)",
                    choices=[str(i) for i in range(1, len(units) + 1)],
                )
                - 1
            )

            from_unit = units[from_idx]
            to_unit = units[to_idx]

            result = convert_unit(value, category, from_unit, to_unit)

            console.print(
                Panel(
                    f"[bold green]{value} {from_unit} = {result:.6f} {to_unit}[/bold green]",
                    title="Conversion Result",
                    border_style="bright_blue",
                )
            )

            save_history(
                {
                    "category": category,
                    "conversion": f"{value} {from_unit} → {result:.6f} {to_unit}",
                }
            )

        elif choice == "2":
            num = IntPrompt.ask("\nEnter a number")
            if is_prime(num):
                console.print(
                    Panel("[bold green]✅ Prime number![/bold green]", title=f"{num}")
                )
            else:
                console.print(
                    Panel("[bold red]❌ Composite number![/bold red]", title=f"{num}")
                )

        elif choice == "3":
            console.print("\n[bold yellow]Solve ax² + bx + c = 0[/bold yellow]")
            a = FloatPrompt.ask("Enter coefficient a (≠ 0)", default=1.0)
            if a == 0:
                console.print("[red]Error: Coefficient 'a' cannot be zero![/red]")
                continue
            b = FloatPrompt.ask("Enter coefficient b", default=0.0)
            c = FloatPrompt.ask("Enter coefficient c", default=0.0)

            result = solve_quadratic(a, b, c)
            console.print(
                Panel(
                    f"[bold cyan]{result}[/bold cyan]",
                    title="Roots",
                    border_style="bright_magenta",
                )
            )

        elif choice == "4":
            if history:
                table = Table(
                    title="Conversion History (newest first)", box=box.SIMPLE_HEAD
                )
                table.add_column("Category", style="cyan")
                table.add_column("Conversion", style="green")
                for entry in reversed(history):
                    table.add_row(entry["category"], entry["conversion"])
                console.print(table)
            else:
                console.print("[yellow]No conversions recorded yet![/yellow]")

        elif choice == "5":
            console.print("[bold magenta]Goodbye! Thank you for using Smart Converter 👋[/bold magenta]")
            break


if __name__ == "__main__":
    main()
