#!/usr/bin/env python3
"""
File Management Utilities
Clean file operations with proper error handling
"""

import json
import os
import uuid


def ensure_directory_exists(path):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False


def generate_safe_filename(title, prompt_id=None):
    """Generate a safe filename from title with length protection"""
    if not prompt_id:
        prompt_id = str(uuid.uuid4())[:8]

    # Clean title for filename
    safe_title = "".join(
        c for c in title if c.isalnum() or c in (" ", "-", "_")
    ).strip()
    safe_title = safe_title.replace(" ", "_").lower()

    # Limit title length to prevent filesystem issues
    # Reserve space for prompt_id (8 chars) + underscore + .json (5 chars) = 14 chars
    # Keep total filename under 200 characters to be safe across filesystems
    max_title_length = 180

    if len(safe_title) > max_title_length:
        # Take first part and add ellipsis indicator
        safe_title = safe_title[:max_title_length].rstrip("_")

    return f"{safe_title}_{prompt_id}.json"


def save_prompt_to_file(prompt_data, filepath):
    """Save prompt data to JSON file"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving file {filepath}: {e}")
        return False


def load_prompt_from_file(filepath):
    """Load prompt data from JSON file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        return None


def find_all_prompts(base_path="prompts"):
    """Find all prompt files in the directory structure"""
    prompts = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                prompt_data = load_prompt_from_file(filepath)
                if prompt_data:
                    prompt_data["_filepath"] = filepath
                    prompts.append(prompt_data)

    return prompts


def delete_prompt_file(filepath):
    """Delete a prompt file"""
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        print(f"Error deleting file {filepath}: {e}")
        return False
