#!/usr/bin/env python3
"""
AI Prompt Manager
Streamlined prompt storage and retrieval with intelligent metadata extraction
"""

import os
import uuid
from datetime import datetime

from metadata_extractor import extract_all_metadata
from utils.cli_helpers import (
    confirm_action,
    display_header,
    display_prompt_summary,
    display_section,
    get_user_choice,
    print_status,
)
from utils.file_helpers import (
    ensure_directory_exists,
    find_all_prompts,
    generate_safe_filename,
    save_prompt_to_file,
)


class PromptManager:
    def __init__(self, base_path="prompts"):
        self.base_path = base_path
        self.public_path = os.path.join(base_path, "public")
        self.private_path = os.path.join(base_path, "private")

        # Ensure directories exist
        ensure_directory_exists(self.public_path)
        ensure_directory_exists(self.private_path)

    def add_prompt(self):
        """Add a new prompt with intelligent metadata extraction"""
        display_header("Add New Prompt")

        print("Paste your complete, optimized prompt below.")
        print("When finished, enter 'END' on a new line:")
        print()

        # Collect prompt content
        content_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                content_lines.append(line)
            except KeyboardInterrupt:
                print_status("\nOperation cancelled", "warning")
                return False

        content = "\n".join(content_lines).strip()

        if not content:
            print_status("No content provided", "error")
            return False

        print_status(f"Content received: {len(content)} characters", "success")

        # Extract metadata intelligently
        display_section("Analyzing Prompt")
        metadata = extract_all_metadata(content)

        # Create prompt data structure
        prompt_data = self._create_prompt_data(content, metadata)

        # Show extracted information and get user confirmation
        self._display_extracted_metadata(prompt_data, metadata)

        # Allow user to modify suggestions
        try:
            prompt_data = self._refine_metadata(prompt_data, metadata)
            if prompt_data is None:  # User cancelled during refinement
                return False
        except KeyboardInterrupt:
            print_status("\nOperation cancelled by user", "warning")
            return False

        # Save the prompt
        if self._save_prompt(prompt_data):
            print_status(
                f"Prompt '{prompt_data['title']}' saved successfully!", "success"
            )
            return True
        else:
            print_status("Failed to save prompt", "error")
            return False

    def _create_prompt_data(self, content, metadata):
        """Create the prompt data structure"""
        prompt_id = str(uuid.uuid4())

        return {
            "id": prompt_id,
            "title": metadata.get("title")
            or metadata.get("ai_suggested_title", "Untitled Prompt"),
            "content": content,
            "category": metadata.get("ai_suggested_category", "general"),
            "tags": metadata.get("ai_suggested_tags", []),
            "private": metadata.get("ai_privacy_recommendation") == "private",
            "description": metadata.get("use_case", ""),
            "created": datetime.now().isoformat(),
            "last_used": None,
            "usage_count": 0,
            "favorite": False,  # New favorites field
            "discovery": metadata.get("discovery", {}),
            "technical_notes": {
                "recommended_llm": metadata.get("recommended_llm"),
                "temperature": metadata.get("temperature"),
                "max_tokens": metadata.get("max_tokens"),
                "additional_notes": metadata.get("additional_notes", []),
            },
            "ai_analysis": {
                "complexity_level": metadata.get("complexity_level"),
                "privacy_reasoning": metadata.get("ai_privacy_reasoning"),
                "suggested_category": metadata.get("ai_suggested_category"),
                "suggested_tags": metadata.get("ai_suggested_tags", []),
            },
        }

    def _display_extracted_metadata(self, prompt_data, metadata):
        """Display the extracted metadata for user review"""
        display_section("Extracted Information")

        print(f"📝 Title: {prompt_data['title']}")
        print(f"📁 Category: {prompt_data['category']}")
        print(
            f"🏷️  Tags: {', '.join(prompt_data['tags']) if prompt_data['tags'] else 'None'}"
        )
        print(f"🔒 Privacy: {'Private' if prompt_data['private'] else 'Public'}")

        if metadata.get("ai_privacy_reasoning"):
            print(f"   └─ Reason: {metadata['ai_privacy_reasoning']}")

        print(f"📊 Complexity: {metadata.get('complexity_level', 'Unknown')}")

        # Technical notes
        tech = prompt_data["technical_notes"]
        if any(tech.values()):
            print("\n🔧 Technical Notes:")
            if tech["recommended_llm"]:
                print(f"   LLM: {tech['recommended_llm']}")
            if tech["temperature"]:
                print(f"   Temperature: {tech['temperature']}")
            if tech["max_tokens"]:
                print(f"   Max Tokens: {tech['max_tokens']}")

        print(
            f"\n📄 Content preview: {prompt_data['content'][:150]}{'...' if len(prompt_data['content']) > 150 else ''}"
        )

    def _refine_metadata(self, prompt_data, metadata):
        """Allow user to refine the extracted metadata"""
        print("\n" + "=" * 50)
        print("REVIEW & MODIFY EXTRACTED INFORMATION")
        print("=" * 50)

        # Title refinement
        if not metadata.get("title"):
            title = input("\nTitle (required): ").strip()
            if title:
                prompt_data["title"] = title
            else:
                prompt_data["title"] = "Untitled Prompt"
        else:
            current_title = prompt_data["title"]
            new_title = input(f"\nTitle [{current_title}]: ").strip()
            if new_title:
                prompt_data["title"] = new_title

        # Category refinement
        current_category = prompt_data["category"]
        new_category = input(f"Category [{current_category}]: ").strip()
        if new_category:
            prompt_data["category"] = new_category

        # Tags refinement
        current_tags = ", ".join(prompt_data["tags"]) if prompt_data["tags"] else ""
        new_tags = input(f"Tags (comma-separated) [{current_tags}]: ").strip()
        if new_tags:
            prompt_data["tags"] = [
                tag.strip() for tag in new_tags.split(",") if tag.strip()
            ]
        elif not prompt_data["tags"]:
            prompt_data["tags"] = []

        # Privacy confirmation with default option
        current_privacy = "Private" if prompt_data["private"] else "Public"
        print(f"\nCurrent privacy setting: {current_privacy}")
        if metadata.get("ai_privacy_reasoning"):
            print(f"AI reasoning: {metadata['ai_privacy_reasoning']}")

        print("\nPrivacy options:")
        print("[1] Keep as suggested (default)")
        print("[2] Make Private")
        print("[3] Make Public")

        while True:
            try:
                choice_input = input("\nChoose privacy setting (1-3) [1]: ").strip()

                # Handle empty input - default to option 1 (keep as suggested)
                if not choice_input:
                    choice = 0  # Keep as suggested
                    break

                choice_num = int(choice_input)
                if choice_num in [1, 2, 3]:
                    choice = choice_num - 1  # Convert to 0-based index
                    break
                else:
                    print("❌ Please enter 1, 2, or 3 (or press Enter for default)")

            except ValueError:
                print(
                    "❌ Please enter a valid number (1, 2, or 3) or press Enter for default"
                )
            except KeyboardInterrupt:
                print_status("\nOperation cancelled by user", "warning")
                return None

        # Apply privacy choice
        if choice == 1:  # Make Private
            prompt_data["private"] = True
        elif choice == 2:  # Make Public
            prompt_data["private"] = False
        # choice == 0 keeps existing setting (default)

        # Description
        current_desc = prompt_data["description"]
        new_desc = input(f"\nDescription [{current_desc}]: ").strip()
        if new_desc:
            prompt_data["description"] = new_desc

        return prompt_data

    def _save_prompt(self, prompt_data):
        """Save prompt to appropriate location"""
        try:
            # Determine save location
            base_location = (
                self.private_path if prompt_data["private"] else self.public_path
            )
            category = prompt_data["category"].lower().replace(" ", "_")
            save_path = os.path.join(base_location, category)

            # Create category directory
            ensure_directory_exists(save_path)

            # Generate filename
            filename = generate_safe_filename(
                prompt_data["title"], prompt_data["id"][:8]
            )
            filepath = os.path.join(save_path, filename)

            # Save file
            if save_prompt_to_file(prompt_data, filepath):
                privacy_label = "Private" if prompt_data["private"] else "Public"
                print(f"\n📁 {privacy_label} prompt saved: {filepath}")
                return True

            return False

        except Exception as e:
            print_status(f"Error saving prompt: {e}", "error")
            return False

    def browse_prompts(self, initial_filter=""):
        """Unified prompt browser with filtering and inline expansion"""
        display_header("📋 Prompt Browser")

        # Get all prompts (unified list)
        all_prompts = find_all_prompts(self.base_path)

        if not all_prompts:
            print_status("No prompts found", "warning")
            return

        # Sort by title for consistent ordering
        all_prompts.sort(key=lambda p: p.get("title", "").lower())

        current_filter = initial_filter

        while True:
            # Apply current filter
            if current_filter:
                filtered_prompts = self._apply_filter(all_prompts, current_filter)
            else:
                filtered_prompts = all_prompts

            # Display filtered browser
            result = self._display_filtered_prompt_browser(
                filtered_prompts, current_filter, len(all_prompts)
            )

            if result == "exit":
                break
            elif result and result.startswith("filter:"):
                current_filter = result[7:]  # Remove "filter:" prefix
            elif result == "clear_filter":
                current_filter = ""

    def _apply_filter(self, prompts, filter_text):
        """Apply filter with smart OR logic and relevance scoring"""
        if not filter_text:
            return prompts

        filter_lower = filter_text.lower().strip()

        # Handle special single-term filters
        if filter_lower in ["⭐", "favorites"]:
            return [p for p in prompts if p.get("favorite", False)]
        if filter_lower == "private":
            return [p for p in prompts if p.get("private", False)]
        if filter_lower == "public":
            return [p for p in prompts if not p.get("private", False)]

        # Multi-term search with OR logic and scoring
        terms = [term for term in filter_lower.split() if len(term) >= 2]
        if not terms:
            return prompts

        # Score each prompt for relevance
        scored_prompts = []

        for prompt in prompts:
            score = 0
            matched_terms = set()

            title = prompt.get("title", "").lower()
            category = prompt.get("category", "").lower()
            tags = [tag.lower() for tag in prompt.get("tags", [])]

            # Get discovery text
            discovery = prompt.get("discovery", {})
            discovery_text = ""
            if discovery:
                discovery_text = (
                    discovery.get("purpose", "").lower()
                    + " "
                    + discovery.get("interaction_style", "").lower()
                    + " "
                    + discovery.get("try_if", "").lower()
                )
                best_for = discovery.get("best_for", "")
                if isinstance(best_for, list):
                    discovery_text += " " + " ".join(best_for).lower()
                elif isinstance(best_for, str):
                    discovery_text += " " + best_for.lower()

            # Score each term
            for term in terms:
                term_score = 0

                # High score: exact title match or title contains term
                if term in title:
                    term_score += 10
                    matched_terms.add(term)

                # Medium-high score: category match
                if term in category:
                    term_score += 7
                    matched_terms.add(term)

                # Medium score: tag match
                if any(term in tag for tag in tags):
                    term_score += 5
                    matched_terms.add(term)

                # Lower score: discovery match (only for 3+ char terms)
                if len(term) >= 3 and term in discovery_text:
                    term_score += 2
                    matched_terms.add(term)

                score += term_score

            # Bonus for matching multiple terms
            if len(matched_terms) > 1:
                score += len(matched_terms) * 2

            # Only include prompts that matched at least one term
            if matched_terms:
                scored_prompts.append((prompt, score, matched_terms))

        # Sort by score (highest first) and return just the prompts
        scored_prompts.sort(key=lambda x: x[1], reverse=True)

        return [prompt for prompt, score, matches in scored_prompts]

    def _display_filtered_prompt_browser(self, prompts, current_filter, total_count):
        """Display the unified prompt browser with filtering and smart refinement"""
        if not prompts:
            if current_filter:
                print_status(f"No prompts found matching '{current_filter}'", "warning")
                choice = (
                    input("\n[Enter] to clear filter or [q] to exit: ").strip().lower()
                )
                return "clear_filter" if choice == "" else "exit"
            else:
                print_status("No prompts found", "warning")
                return "exit"

        # Smart refinement suggestion for too many results
        if len(prompts) > 15 and current_filter and len(current_filter) <= 3:
            print_status(
                f"Found {len(prompts)} results for '{current_filter}' - consider refining your search",
                "info",
            )
            print(
                "💡 Try: '{current_filter} strategy', '{current_filter} coaching', or '{current_filter} productivity'"
            )
            refine = input("\nRefine search or [Enter] to view all results: ").strip()
            if refine:
                return f"filter:{current_filter} {refine}"

        # Track expanded state for each prompt
        expanded_prompts = set()

        while True:
            # Clear screen for clean display
            print("\033[2J\033[H", end="")

            print("\n" + "=" * 70)
            print(f"📋 PROMPT BROWSER ({total_count} prompts)")
            print("=" * 70)

            # Show filter status
            if current_filter:
                print(
                    f"🔍 Filter: {current_filter}                              [x] Clear"
                )
            else:
                print("🔍 Filter: [                    ] [Enter to search]")
            print()

            # Count public/private in filtered results
            public_count = len([p for p in prompts if not p.get("private", False)])
            private_count = len([p for p in prompts if p.get("private", False)])

            # Display prompts with inline expansion
            for i, prompt in enumerate(prompts, 1):
                title = prompt.get("title", "Untitled")

                # Add star indicator
                if prompt.get("favorite", False):
                    title = f"⭐ {title}"

                # Privacy indicator
                privacy_icon = "🔒" if prompt.get("private", False) else "🌐"
                privacy_label = "Private" if prompt.get("private", False) else "Public"

                is_expanded = i in expanded_prompts

                # Show prompt title with privacy
                if is_expanded:
                    print(f"\n[{i}] {title} [EXPANDED]")
                else:
                    print(f"\n[{i}] {title}")

                category = prompt.get("category", "general")
                print(f"    📁 {category} • {privacy_icon} {privacy_label}")

                # Show discovery info if expanded
                if is_expanded:
                    discovery = prompt.get("discovery", {})
                    if discovery and isinstance(discovery, dict):
                        if discovery.get("purpose"):
                            print(f"    💡 {discovery['purpose']}")

                        # Combine key info on one line
                        info_parts = []
                        if discovery.get("session_length"):
                            info_parts.append(f"⏱️ {discovery['session_length']}")
                        if discovery.get("interaction_style"):
                            info_parts.append(f"🎭 {discovery['interaction_style']}")

                        if info_parts:
                            print(f"    {' • '.join(info_parts)}")

                        if discovery.get("try_if"):
                            print(f"    🤔 Try if: {discovery['try_if']}")

                    # Add technical info to expanded view
                    tech = prompt.get("technical_notes", {})
                    if tech and isinstance(tech, dict):
                        tech_parts = []
                        if tech.get("recommended_llm"):
                            tech_parts.append(tech["recommended_llm"])
                        if tech.get("temperature") is not None:
                            tech_parts.append(f"{tech['temperature']} temp")
                        if tech.get("max_tokens"):
                            tech_parts.append(f"{tech['max_tokens']} tokens")

                        if tech_parts:
                            print(f"    🔧 {' • '.join(tech_parts)}")

                    # Show quick actions for expanded prompts
                    is_favorite = prompt.get("favorite", False)
                    fav_icon = "⭐" if is_favorite else "☆"
                    fav_action = "unfav" if is_favorite else "fav"
                    print(
                        f"    ➤ [{i}f] Full  [{i}c] Copy  [{i}p] Project  [{i}{fav_action}] {fav_icon}"
                    )

            print("\n" + "=" * 70)

            # Show summary
            if current_filter:
                print(
                    f"📊 {len(prompts)} results: {public_count} public • {private_count} private"
                )
            else:
                print(
                    f"📊 {len(prompts)} prompts: {public_count} public • {private_count} private"
                )

            print("📝 Commands:")
            if current_filter:
                print("  • [number] = toggle info • [x] = clear filter")
            else:
                print(
                    "  • [number] = toggle info • Type text to filter (OR logic, scored by relevance)"
                )
            print(
                "  • [number]f = full • [number]c = copy • [number]p = Claude Project • [⭐] = favorites"
            )
            print("  • [q] = back to main menu")

            choice = input("\n🎯 Command: ").strip()

            if choice.lower() == "q" or not choice:
                return "exit"
            elif choice.lower() == "x" and current_filter:
                return "clear_filter"
            elif choice == "⭐":
                return "filter:⭐"
            elif choice.lower() in ["private", "public", "favorites"]:
                return f"filter:{choice.lower()}"
            elif choice.endswith("f"):
                # Show full prompt content
                try:
                    num = int(choice[:-1])
                    if 1 <= num <= len(prompts):
                        idx = num - 1
                        self._show_full_prompt_content(prompts[idx])
                        input("Press Enter to continue...")
                    else:
                        print_status(f"Invalid prompt number: {num}", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    print_status("Invalid format. Use number+f (e.g., '3f')", "error")
                    input("Press Enter to continue...")
            elif choice.endswith("c"):
                # Copy prompt
                try:
                    num = int(choice[:-1])
                    if 1 <= num <= len(prompts):
                        idx = num - 1
                        self._copy_to_clipboard(prompts[idx]["content"])
                        input("Press Enter to continue...")
                    else:
                        print_status(f"Invalid prompt number: {num}", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    print_status("Invalid format. Use number+c (e.g., '3c')", "error")
                    input("Press Enter to continue...")
            elif choice.endswith("p"):
                # Copy for Claude Project
                try:
                    num = int(choice[:-1])
                    if 1 <= num <= len(prompts):
                        idx = num - 1
                        self._copy_for_claude_project(prompts[idx])
                        input("Press Enter to continue...")
                    else:
                        print_status(f"Invalid prompt number: {num}", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    print_status("Invalid format. Use number+p (e.g., '3p')", "error")
                    input("Press Enter to continue...")
            elif choice.endswith("fav") or choice.endswith("unfav"):
                # Toggle favorite
                try:
                    if choice.endswith("fav"):
                        num = int(choice[:-3])
                    else:
                        num = int(choice[:-5])

                    if 1 <= num <= len(prompts):
                        idx = num - 1
                        self._toggle_favorite(prompts[idx])
                        input("Press Enter to continue...")
                    else:
                        print_status(f"Invalid prompt number: {num}", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    print_status(
                        "Invalid format. Use number+fav (e.g., '3fav')", "error"
                    )
                    input("Press Enter to continue...")
            elif choice.isdigit():
                # Toggle expansion
                num = int(choice)
                if 1 <= num <= len(prompts):
                    if num in expanded_prompts:
                        expanded_prompts.remove(num)
                    else:
                        expanded_prompts.add(num)
                    # Immediate redraw - no pause
                else:
                    print_status(f"Invalid prompt number: {num}", "error")
                    input("Press Enter to continue...")
            elif not current_filter and choice:
                # Apply new filter - strip any brackets
                clean_choice = choice.strip("[]")
                return f"filter:{clean_choice}"

    def _display_prompt_list(self, prompts, show_stars=False):
        """Display a list of prompts with smooth inline expansion"""
        if not prompts:
            print_status("No prompts found", "info")
            return

        # Track expanded state for each prompt
        expanded_prompts = set()

        while True:
            # Clear screen for clean display
            print("\033[2J\033[H", end="")  # Clear screen and move cursor to top

            print("\n" + "=" * 70)
            print("📋 PROMPT BROWSER")
            print("=" * 70)

            # Display prompts with inline expansion
            for i, prompt in enumerate(prompts, 1):
                title = prompt.get("title", "Untitled")

                # Add star indicator
                if prompt.get("favorite", False):
                    title = f"⭐ {title}"

                is_expanded = i in expanded_prompts

                # Show prompt title
                if is_expanded:
                    print(f"\n[{i}] {title} [EXPANDED]")
                else:
                    print(f"\n[{i}] {title}")

                # Show basic info always
                category = prompt.get("category", "general")
                privacy = "Private" if prompt.get("private", False) else "Public"
                print(f"    📁 {category} • 🔒 {privacy}")

                # Show discovery info if expanded
                if is_expanded:
                    discovery = prompt.get("discovery", {})
                    if discovery and isinstance(discovery, dict):
                        if discovery.get("purpose"):
                            print(f"    💡 {discovery['purpose']}")

                        # Combine key info on one line
                        info_parts = []
                        if discovery.get("session_length"):
                            info_parts.append(f"⏱️ {discovery['session_length']}")
                        if discovery.get("interaction_style"):
                            info_parts.append(f"🎭 {discovery['interaction_style']}")

                        if info_parts:
                            print(f"    {' • '.join(info_parts)}")

                        if discovery.get("try_if"):
                            print(f"    🤔 Try if: {discovery['try_if']}")

                    # Add technical info to expanded view
                    tech = prompt.get("technical_notes", {})
                    if tech and isinstance(tech, dict):
                        tech_parts = []
                        if tech.get("recommended_llm"):
                            tech_parts.append(tech["recommended_llm"])
                        if tech.get("temperature") is not None:
                            tech_parts.append(f"{tech['temperature']} temp")
                        if tech.get("max_tokens"):
                            tech_parts.append(f"{tech['max_tokens']} tokens")

                        if tech_parts:
                            print(f"    🔧 {' • '.join(tech_parts)}")

                    # Show quick actions for expanded prompts
                    is_favorite = prompt.get("favorite", False)
                    fav_icon = "⭐" if is_favorite else "☆"
                    fav_action = "unfav" if is_favorite else "fav"
                    print(
                        f"    ➤ [{i}f] Full prompt  [{i}c] Copy prompt  [{i}{fav_action}] {fav_icon} Favorite"
                    )

            print("\n" + "=" * 70)
            print("📝 Commands:")
            print("  • [number] = toggle discovery info (e.g., '3')")
            print("  • [number]f = full prompt content (e.g., '3f')")
            print("  • [number]c = copy prompt (e.g., '3c')")
            print("  • [number]fav/unfav = toggle favorite (e.g., '3fav')")
            print("  • [q] = back to main menu")

            choice = input("\n🎯 Command: ").strip().lower()

            if choice == "q" or not choice:
                # Return to main menu
                break
            elif choice.endswith("f"):
                # Show full prompt content
                try:
                    num = int(choice[:-1])
                    if 1 <= num <= len(prompts):
                        idx = num - 1
                        self._show_full_prompt_content(prompts[idx])
                        input("Press Enter to continue...")
                    else:
                        print_status(f"Invalid prompt number: {num}", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    print_status("Invalid format. Use number+f (e.g., '3f')", "error")
                    input("Press Enter to continue...")
            elif choice.endswith("c"):
                # Copy prompt
                try:
                    num = int(choice[:-1])
                    if 1 <= num <= len(prompts):
                        idx = num - 1
                        self._copy_to_clipboard(prompts[idx]["content"])
                        input("Press Enter to continue...")
                    else:
                        print_status(f"Invalid prompt number: {num}", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    print_status("Invalid format. Use number+c (e.g., '3c')", "error")
                    input("Press Enter to continue...")
            elif choice.endswith("fav") or choice.endswith("unfav"):
                # Toggle favorite
                try:
                    if choice.endswith("fav"):
                        num = int(choice[:-3])  # Remove 'fav'
                    else:
                        num = int(choice[:-5])  # Remove 'unfav'

                    if 1 <= num <= len(prompts):
                        idx = num - 1
                        self._toggle_favorite(prompts[idx])
                        input("Press Enter to continue...")
                    else:
                        print_status(f"Invalid prompt number: {num}", "error")
                        input("Press Enter to continue...")
                except ValueError:
                    print_status(
                        "Invalid format. Use number+fav or number+unfav (e.g., '3fav')",
                        "error",
                    )
                    input("Press Enter to continue...")
            elif choice.isdigit():
                # Toggle expansion
                num = int(choice)
                if 1 <= num <= len(prompts):
                    if num in expanded_prompts:
                        expanded_prompts.remove(num)
                    else:
                        expanded_prompts.add(num)
                    # Immediate redraw - no pause
                else:
                    print_status(f"Invalid prompt number: {num}", "error")
                    input("Press Enter to continue...")
            else:
                print_status(
                    "Invalid command. Use number, numberf, numberc, or q", "error"
                )
                input("Press Enter to continue...")

    def _show_full_prompt_content(self, prompt_data):
        """Show the complete prompt content in a clean format"""
        title = prompt_data.get("title", "Untitled")

        # Clear screen for clean view
        print("\033[2J\033[H", end="")

        print("\n" + "=" * 70)
        print(f"📋 {title}")
        print("=" * 70)

        # Show the complete prompt content
        content = prompt_data.get("content", "No content available")
        print(content)

        print("\n" + "─" * 70)

        # Quick actions at bottom
        is_favorite = prompt_data.get("favorite", False)
        fav_icon = "⭐" if is_favorite else "☆"
        fav_action = "Remove from" if is_favorite else "Add to"

        print(
            f"[c] Copy to clipboard  [p] Copy for Claude Project  [{fav_icon}] {fav_action} favorites  [q] Back to browser"
        )

        while True:
            action = input("\n🎯 Action: ").strip().lower()

            if action == "c":
                self._copy_to_clipboard(content)
                break
            elif action == "p":
                self._copy_for_claude_project(prompt_data)
                break
            elif action == fav_icon or action == "star" or action == "fav":
                self._toggle_favorite(prompt_data)
                break
            elif action == "q" or action == "":
                break
            else:
                print_status("Invalid action. Use 'c', 'p', 'fav', or 'q'", "error")

    def _show_detailed_prompt(self, prompt_data):
        """Show detailed view of a specific prompt"""
        display_section("Detailed Prompt View")
        display_prompt_summary(prompt_data)

        # Show AI analysis if available
        ai_analysis = prompt_data.get("ai_analysis", {})
        if ai_analysis:
            print("🤖 AI Analysis:")
            if ai_analysis.get("complexity_level"):
                print(f"   • Complexity: {ai_analysis['complexity_level']}")
            if ai_analysis.get("privacy_reasoning"):
                print(f"   • Privacy reasoning: {ai_analysis['privacy_reasoning']}")
            print()

        # Options for this prompt
        is_favorite = prompt_data.get("favorite", False)
        favorite_action = "Remove from favorites" if is_favorite else "Add to favorites"

        print("Actions:")
        print("[1] Copy content to clipboard")
        print("[2] Show full content")
        print("[3] Edit metadata")
        print(f"[4] ⭐ {favorite_action}")
        print("[5] Change privacy setting")
        print("[6] Delete prompt")
        print("[7] Back to list")

        options = [
            "Copy to clipboard",
            "Show full content",
            "Edit metadata",
            favorite_action,
            "Change privacy setting",
            "Delete prompt",
            "Back to list",
        ]
        choice = get_user_choice(options, "Select action")

        if choice == 0:  # Copy to clipboard
            self._copy_to_clipboard(prompt_data["content"])
        elif choice == 1:  # Show full content
            self._show_full_content(prompt_data)
        elif choice == 2:  # Edit metadata
            print_status("Metadata editing coming soon", "info")
        elif choice == 3:  # Toggle favorite
            self._toggle_favorite(prompt_data)
        elif choice == 4:  # Change privacy setting
            self._change_privacy_setting(prompt_data)
        elif choice == 5:  # Delete prompt
            self._delete_prompt(prompt_data)
        # choice == 6 returns to list

    def _copy_to_clipboard(self, content):
        """Copy content to clipboard if possible"""
        try:
            import pyperclip

            pyperclip.copy(content)
            print_status("Content copied to clipboard!", "success")
        except ImportError:
            print_status(
                "Clipboard functionality requires 'pyperclip' package", "warning"
            )
            print("Install with: pip install pyperclip")
            print("\nContent to copy:")
            print("-" * 50)
            print(content)
            print("-" * 50)

    def _copy_for_claude_project(self, prompt_data):
        """Format and copy prompt for Claude Project setup"""
        title = prompt_data.get("title", "Untitled")
        content = prompt_data.get("content", "")
        category = prompt_data.get("category", "general")

        # Build formatted output for Claude Project
        project_content = []
        project_content.append("=" * 70)
        project_content.append("CUSTOM INSTRUCTIONS FOR CLAUDE PROJECT")
        project_content.append("=" * 70)
        project_content.append("")
        project_content.append(content)
        project_content.append("")
        project_content.append("=" * 70)
        project_content.append(f"Source: {title}")
        project_content.append(f"Category: {category}")

        # Add discovery info if available
        discovery = prompt_data.get("discovery", {})
        if discovery and isinstance(discovery, dict):
            if discovery.get("purpose"):
                project_content.append(f"Purpose: {discovery['purpose']}")

        project_content.append("=" * 70)

        formatted_content = "\n".join(project_content)

        # Copy to clipboard
        try:
            import pyperclip

            pyperclip.copy(formatted_content)
            print_status(
                "\n✅ Formatted for Claude Project and copied to clipboard!", "success"
            )
            print("\n📖 Next steps:")
            print("   1. Go to Claude.ai")
            print("   2. Click 'Projects' in the left sidebar")
            print("   3. Click '+ New Project'")
            print(f"   4. Name your project (e.g., '{title}')")
            print("   5. Click 'Set custom instructions'")
            print("   6. Paste the copied content (Cmd+V / Ctrl+V)")
            print("   7. Save and start a new chat in that project!")
            print(
                "\n🚀 Your prompt will now be active for every conversation in that project."
            )
        except ImportError:
            print_status(
                "Clipboard functionality requires 'pyperclip' package", "warning"
            )
            print("Install with: pip install pyperclip")
            print("\nContent formatted for Claude Project:")
            print(formatted_content)

    def _show_full_content(self, prompt_data):
        """Show the full prompt content"""
        display_section(f"Full Content: {prompt_data['title']}")
        print(prompt_data["content"])
        print("\n" + "=" * 60)
        input("Press Enter to continue...")

    def _delete_prompt(self, prompt_data):
        """Delete a prompt with confirmation"""
        title = prompt_data.get("title", "Unknown")

        if confirm_action(f"Are you sure you want to delete '{title}'?", default="n"):
            # Find and delete the file
            filepath = prompt_data.get("_filepath")
            if filepath and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    print_status(f"Deleted '{title}'", "success")
                except Exception as e:
                    print_status(f"Error deleting file: {e}", "error")
            else:
                print_status("Could not locate file to delete", "error")
        else:
            print_status("Deletion cancelled", "info")

    def _change_privacy_setting(self, prompt_data):
        """Change privacy setting for a prompt"""
        title = prompt_data.get("title", "Unknown")
        current_privacy = "Private" if prompt_data.get("private", False) else "Public"
        new_privacy = "Public" if current_privacy == "Private" else "Private"

        display_section(f"Change Privacy: {title}")
        print(f"Current setting: {current_privacy}")
        print(f"New setting: {new_privacy}")

        # Show privacy implications
        if new_privacy == "Private":
            print("\n📝 Moving to Private:")
            print("   • Will be stored in git-ignored private folder")
            print("   • Not visible in public repository")
            print("   • Only accessible locally")
        else:
            print("\n📝 Moving to Public:")
            print("   • Will be stored in git-tracked public folder")
            print("   • Visible in public repository")
            print("   • Shareable with others")
            print("\n⚠️  WARNING: Ensure this prompt contains no personal details,")
            print("   company-specific info, or individual characteristics!")

        if confirm_action(
            f"Change '{title}' from {current_privacy} to {new_privacy}?", default="n"
        ):
            success = self._move_prompt_privacy(prompt_data, new_privacy == "Private")
            if success:
                print_status(f"'{title}' moved to {new_privacy}", "success")
            else:
                print_status("Failed to change privacy setting", "error")
        else:
            print_status("Privacy change cancelled", "info")

    def _move_prompt_privacy(self, prompt_data, make_private):
        """Move prompt between public and private folders"""
        try:
            # Get current and new paths
            current_filepath = prompt_data.get("_filepath")
            if not current_filepath or not os.path.exists(current_filepath):
                print_status("Cannot locate current prompt file", "error")
                return False

            # Update privacy setting in data
            prompt_data["private"] = make_private

            # Determine new location
            base_location = self.private_path if make_private else self.public_path
            category = prompt_data.get("category", "general").lower().replace(" ", "_")
            new_directory = os.path.join(base_location, category)

            # Create new directory if needed
            ensure_directory_exists(new_directory)

            # Generate new filename (keep same ID)
            title = prompt_data.get("title", "untitled")
            prompt_id = prompt_data.get("id", "unknown")[:8]
            new_filename = generate_safe_filename(title, prompt_id)
            new_filepath = os.path.join(new_directory, new_filename)

            # Save to new location
            if save_prompt_to_file(prompt_data, new_filepath):
                # Remove old file
                try:
                    os.remove(current_filepath)
                    privacy_label = "Private" if make_private else "Public"
                    print(f"📁 Moved to {privacy_label}: {new_filepath}")
                    return True
                except Exception as e:
                    print_status(f"Warning: Could not remove old file: {e}", "warning")
                    print_status("Prompt saved to new location successfully", "success")
                    return True
            else:
                return False

        except Exception as e:
            print_status(f"Error moving prompt: {e}", "error")
            return False

    def search_prompts(self):
        """Search prompts and open browser with filter applied"""
        display_header("🔍 Search Prompts")

        search_query = input(
            "Enter search term (title, category, content, or tag): "
        ).strip()

        if not search_query:
            print_status("No search term provided", "warning")
            return

        print_status(f"Searching for: '{search_query}'", "processing")

        # Open browser with search filter applied
        self.browse_prompts(initial_filter=search_query)

    def _toggle_favorite(self, prompt_data):
        """Toggle favorite status for a prompt"""
        title = prompt_data.get("title", "Unknown")
        current_favorite = prompt_data.get("favorite", False)
        new_status = not current_favorite

        # Update favorite status
        prompt_data["favorite"] = new_status

        # Save updated prompt
        filepath = prompt_data.get("_filepath")
        if filepath and save_prompt_to_file(prompt_data, filepath):
            action = "Added to" if new_status else "Removed from"
            print_status(f"{action} favorites: '{title}' ⭐", "success")
        else:
            print_status(f"Failed to update favorite status for '{title}'", "error")


if __name__ == "__main__":
    print("⚠️  This module should be imported, not run directly.")
    print("📝 To use AI Prompt Manager, run: python main.py")
