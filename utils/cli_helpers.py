#!/usr/bin/env python3
"""
Enhanced CLI Helper Functions
Professional terminal interface patterns from the automation template
"""

def print_header(title, subtitle=None, width=60):
    """Print a formatted header"""
    print("\n" + "=" * width)
    print(title)
    print("=" * width)
    if subtitle:
        print(subtitle)
        print()

def print_section(title, width=50):
    """Print a section divider"""
    print("\n" + "-" * width)
    print(title)
    print("-" * width)

def show_menu_options(options):
    """Display menu options in consistent format"""
    print("\nOptions:")
    for i, option in enumerate(options, 1):
        print(f"[{i}] {option}")

def get_user_choice(options, prompt="Select option"):
    """Get validated user choice from menu"""
    max_choice = len(options)
    
    while True:
        try:
            choice = input(f"\n{prompt} (1-{max_choice}): ").strip()
            
            # Handle empty input
            if not choice:
                print("❌ Please enter a number to make your selection.")
                continue
                
            # Try to convert to integer
            index = int(choice) - 1
            
            if 0 <= index < max_choice:
                return index
            else:
                print(f"❌ Invalid choice. Please select 1-{max_choice}.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user. Goodbye!")
            raise KeyboardInterrupt()  # Re-raise to propagate up
        except ValueError:
            print(f"❌ Please enter a valid number between 1 and {max_choice}.")

def confirm_action(message, default="n"):
    """Get user confirmation for destructive actions"""
    choices = "y/N" if default.lower() == "n" else "Y/n"
    response = input(f"{message} ({choices}): ").strip().lower()
    
    if not response:
        return default.lower() == "y"
    
    return response in ['y', 'yes']

def print_status(message, status_type="info"):
    """Print status messages with consistent formatting"""
    icons = {
        "success": "✅",
        "error": "❌", 
        "warning": "⚠️",
        "info": "ℹ️",
        "processing": "🔄"
    }
    
    icon = icons.get(status_type, "•")
    print(f"{icon} {message}")

def display_header(title):
    """Display a formatted header"""
    print_header(title)

def display_section(title):
    """Display a section divider"""
    print_section(title)

def display_table(headers, rows, max_width=100):
    """Display data in table format with proper spacing"""
    if not rows:
        print("No data to display")
        return
    
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Adjust widths to fit max_width if needed
    total_width = sum(col_widths) + len(headers) * 3 - 1
    if total_width > max_width:
        excess = total_width - max_width
        # Reduce longest columns first
        while excess > 0 and max(col_widths) > 10:
            longest_idx = col_widths.index(max(col_widths))
            col_widths[longest_idx] -= 1
            excess -= 1
    
    # Print header
    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))
    print(f"\n{header_row}")
    print("-" * len(header_row))
    
    # Print rows
    for row in rows:
        data_row = " | ".join(str(cell)[:width].ljust(width) for cell, width in zip(row, col_widths))
        print(data_row)
    
    print()

def handle_keyboard_interrupt():
    """Handle Ctrl+C gracefully"""
    print("\n\n👋 Operation cancelled by user. Goodbye!")
    return None

def validate_input(prompt, validator_func, error_message="Invalid input"):
    """Get validated input from user"""
    while True:
        user_input = input(prompt).strip()
        
        if validator_func(user_input):
            return user_input
        else:
            print_status(error_message, "error")

def display_prompt_summary(prompt_data):
    """Display a formatted prompt summary"""
    print(f"\n📝 {prompt_data.get('title', 'Untitled')}")
    print(f"📁 Category: {prompt_data.get('category', 'general')}")
    
    tags = prompt_data.get('tags', [])
    if tags and isinstance(tags, list):
        print(f"🏷️  Tags: {', '.join(str(tag) for tag in tags)}")
    
    privacy = "Private" if prompt_data.get('private', False) else "Public"
    print(f"🔒 Privacy: {privacy}")
    
    # Technical details - handle None values safely
    tech = prompt_data.get('technical_notes', {})
    if tech and isinstance(tech, dict) and any(v for v in tech.values() if v is not None):
        print("🔧 Technical:")
        if tech.get('recommended_llm'):
            print(f"   • LLM: {tech['recommended_llm']}")
        if tech.get('temperature') is not None:
            print(f"   • Temperature: {tech['temperature']}")
        if tech.get('max_tokens'):
            print(f"   • Max Tokens: {tech['max_tokens']}")
    
    # Content preview
    content = prompt_data.get('content', '')
    preview_length = 200
    if len(content) > preview_length:
        preview = content[:preview_length] + "..."
    else:
        preview = content
    
    print(f"\n📄 Content Preview:")
    print(f"   {preview}")
    print()
