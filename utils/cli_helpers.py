#!/usr/bin/env python3
"""
Enhanced CLI Helper Functions using Rich
Professional terminal interface with consistent formatting
"""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

# Global console instance
console = Console()


def print_header(title, subtitle=None, width=60):
    """Print a formatted header with Rich"""
    if subtitle:
        panel = Panel(
            f"[bold]{title}[/bold]\n{subtitle}", border_style="blue", box=box.DOUBLE
        )
    else:
        panel = Panel(f"[bold]{title}[/bold]", border_style="blue", box=box.DOUBLE)
    console.print(panel)


def print_section(title, width=50):
    """Print a section divider with Rich"""
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print("─" * width, style="dim")


def print_status(message, status_type="info"):
    """Print status messages with Rich styling"""
    styles = {
        "success": "[bold green]✅",
        "error": "[bold red]❌",
        "warning": "[bold yellow]⚠️",
        "info": "[bold blue]ℹ️",
        "processing": "[bold cyan]🔄",
    }

    style = styles.get(status_type, "•")
    console.print(f"{style} {message}")


def show_menu_options(options):
    """Display menu options in consistent format"""
    console.print("\n[bold cyan]Options:[/bold cyan]")
    for i, option in enumerate(options, 1):
        console.print(f"[{i}] {option}")


def get_user_choice(options, prompt="Select option"):
    """Get validated user choice from menu"""
    max_choice = len(options)

    while True:
        try:
            choice = input(f"\n{prompt} (1-{max_choice}): ").strip()

            # Handle empty input
            if not choice:
                print_status("Please enter a number to make your selection.", "error")
                continue

            # Try to convert to integer
            index = int(choice) - 1

            if 0 <= index < max_choice:
                return index
            else:
                print_status(f"Invalid choice. Please select 1-{max_choice}.", "error")

        except KeyboardInterrupt:
            console.print(
                "\n\n👋 Operation cancelled by user. Goodbye!", style="bold yellow"
            )
            raise KeyboardInterrupt()  # Re-raise to propagate up
        except ValueError:
            print_status(
                f"Please enter a valid number between 1 and {max_choice}.", "error"
            )


def confirm_action(message, default="n"):
    """Get user confirmation with Rich prompt"""
    default_bool = default.lower() == "y"
    return Confirm.ask(message, default=default_bool)


def get_input(prompt_text, default=None):
    """Get user input with Rich prompt"""
    if default:
        return Prompt.ask(prompt_text, default=default)
    return Prompt.ask(prompt_text)


def display_table(headers, rows, title=None):
    """Display data in Rich table format"""
    table = Table(title=title, box=box.ROUNDED)

    for header in headers:
        table.add_column(header, style="cyan", no_wrap=False)

    for row in rows:
        table.add_row(*[str(cell) for cell in row])

    console.print(table)


def display_prompt_summary(prompt_data):
    """Display a formatted prompt summary with Rich"""
    title = prompt_data.get("title", "Untitled")
    category = prompt_data.get("category", "general")
    privacy = "Private 🔒" if prompt_data.get("private", False) else "Public 🌐"

    # Build summary text
    summary = f"[bold]{title}[/bold]\n\n"
    summary += f"📁 Category: {category}\n"
    summary += f"{privacy}\n"

    tags = prompt_data.get("tags", [])
    if tags:
        summary += f"🏷️  Tags: {', '.join(tags)}\n"

    # Discovery info
    discovery = prompt_data.get("discovery", {})
    if discovery:
        summary += "\n[bold cyan]💡 Discovery[/bold cyan]\n"
        if discovery.get("purpose"):
            summary += f"  Purpose: {discovery['purpose']}\n"
        if discovery.get("try_if"):
            summary += f"  Try if: {discovery['try_if']}\n"

    # Technical info
    tech = prompt_data.get("technical_notes", {})
    if tech and any(tech.values()):
        summary += "\n[bold cyan]🔧 Technical[/bold cyan]\n"
        if tech.get("recommended_llm"):
            summary += f"  LLM: {tech['recommended_llm']}\n"
        if tech.get("temperature") is not None:
            summary += f"  Temperature: {tech['temperature']}\n"

    panel = Panel(summary, border_style="green", box=box.ROUNDED)
    console.print(panel)


# Keep backwards compatibility
display_header = print_header
display_section = print_section


def handle_keyboard_interrupt():
    """Handle Ctrl+C gracefully"""
    console.print("\n\n👋 Operation cancelled by user. Goodbye!", style="bold yellow")
    return None


def validate_input(prompt, validator_func, error_message="Invalid input"):
    """Get validated input from user"""
    while True:
        user_input = input(prompt).strip()

        if validator_func(user_input):
            return user_input
        else:
            print_status(error_message, "error")
