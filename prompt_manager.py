#!/usr/bin/env python3
"""
AI Prompt Manager V2
Streamlined prompt storage and retrieval with intelligent metadata extraction
"""

import os
import uuid
from datetime import datetime
from utils.cli_helpers import print_status, get_user_choice, confirm_action, display_header, display_section, display_table, display_prompt_summary
from utils.file_helpers import ensure_directory_exists, generate_safe_filename, save_prompt_to_file, find_all_prompts
from metadata_extractor import extract_all_metadata

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
        display_header("Add New Prompt - V2")
        
        print("Paste your complete, optimized prompt below.")
        print("When finished, enter 'END' on a new line:")
        print()
        
        # Collect prompt content
        content_lines = []
        while True:
            try:
                line = input()
                if line.strip() == 'END':
                    break
                content_lines.append(line)
            except KeyboardInterrupt:
                print_status("\nOperation cancelled", "warning")
                return False
        
        content = '\n'.join(content_lines).strip()
        
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
            print_status(f"Prompt '{prompt_data['title']}' saved successfully!", "success")
            return True
        else:
            print_status("Failed to save prompt", "error")
            return False
    
    def _create_prompt_data(self, content, metadata):
        """Create the prompt data structure"""
        prompt_id = str(uuid.uuid4())
        
        return {
            'id': prompt_id,
            'title': metadata.get('title', 'Untitled Prompt'),
            'content': content,
            'category': metadata.get('ai_suggested_category', 'general'),
            'tags': metadata.get('ai_suggested_tags', []),
            'private': metadata.get('ai_privacy_recommendation') == 'private',
            'description': metadata.get('use_case', ''),
            'created': datetime.now().isoformat(),
            'last_used': None,
            'usage_count': 0,
            'technical_notes': {
                'recommended_llm': metadata.get('recommended_llm'),
                'temperature': metadata.get('temperature'),
                'max_tokens': metadata.get('max_tokens'),
                'additional_notes': metadata.get('additional_notes', [])
            },
            'ai_analysis': {
                'complexity_level': metadata.get('complexity_level'),
                'privacy_reasoning': metadata.get('ai_privacy_reasoning'),
                'suggested_category': metadata.get('ai_suggested_category'),
                'suggested_tags': metadata.get('ai_suggested_tags', [])
            }
        }
    
    def _display_extracted_metadata(self, prompt_data, metadata):
        """Display the extracted metadata for user review"""
        display_section("Extracted Information")
        
        print(f"📝 Title: {prompt_data['title']}")
        print(f"📁 Category: {prompt_data['category']}")
        print(f"🏷️  Tags: {', '.join(prompt_data['tags']) if prompt_data['tags'] else 'None'}")
        print(f"🔒 Privacy: {'Private' if prompt_data['private'] else 'Public'}")
        
        if metadata.get('ai_privacy_reasoning'):
            print(f"   └─ Reason: {metadata['ai_privacy_reasoning']}")
        
        print(f"📊 Complexity: {metadata.get('complexity_level', 'Unknown')}")
        
        # Technical notes
        tech = prompt_data['technical_notes']
        if any(tech.values()):
            print("\n🔧 Technical Notes:")
            if tech['recommended_llm']:
                print(f"   LLM: {tech['recommended_llm']}")
            if tech['temperature']:
                print(f"   Temperature: {tech['temperature']}")
            if tech['max_tokens']:
                print(f"   Max Tokens: {tech['max_tokens']}")
        
        print(f"\n📄 Content preview: {prompt_data['content'][:150]}{'...' if len(prompt_data['content']) > 150 else ''}")
    
    def _refine_metadata(self, prompt_data, metadata):
        """Allow user to refine the extracted metadata"""
        print("\n" + "="*50)
        print("REVIEW & MODIFY EXTRACTED INFORMATION")
        print("="*50)
        
        # Title refinement
        if not metadata.get('title'):
            title = input("\nTitle (required): ").strip()
            if title:
                prompt_data['title'] = title
            else:
                prompt_data['title'] = "Untitled Prompt"
        else:
            current_title = prompt_data['title']
            new_title = input(f"\nTitle [{current_title}]: ").strip()
            if new_title:
                prompt_data['title'] = new_title
        
        # Category refinement
        current_category = prompt_data['category']
        new_category = input(f"Category [{current_category}]: ").strip()
        if new_category:
            prompt_data['category'] = new_category
        
        # Tags refinement
        current_tags = ', '.join(prompt_data['tags']) if prompt_data['tags'] else ''
        new_tags = input(f"Tags (comma-separated) [{current_tags}]: ").strip()
        if new_tags:
            prompt_data['tags'] = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
        elif not prompt_data['tags']:
            prompt_data['tags'] = []
        
        # Privacy confirmation with default option
        current_privacy = 'Private' if prompt_data['private'] else 'Public'
        print(f"\nCurrent privacy setting: {current_privacy}")
        if metadata.get('ai_privacy_reasoning'):
            print(f"AI reasoning: {metadata['ai_privacy_reasoning']}")
        
        print("\nPrivacy options:")
        print("[1] Keep as suggested (default)")
        print("[2] Make Private") 
        print("[3] Make Public")
        
        while True:
            try:
                choice_input = input(f"\nChoose privacy setting (1-3) [1]: ").strip()
                
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
                print("❌ Please enter a valid number (1, 2, or 3) or press Enter for default")
            except KeyboardInterrupt:
                print_status("\nOperation cancelled by user", "warning")
                return None
        
        # Apply privacy choice
        if choice == 1:  # Make Private
            prompt_data['private'] = True
        elif choice == 2:  # Make Public
            prompt_data['private'] = False
        # choice == 0 keeps existing setting (default)
        
        # Description
        current_desc = prompt_data['description']
        new_desc = input(f"\nDescription [{current_desc}]: ").strip()
        if new_desc:
            prompt_data['description'] = new_desc
        
        return prompt_data
    
    def _save_prompt(self, prompt_data):
        """Save prompt to appropriate location"""
        try:
            # Determine save location
            base_location = self.private_path if prompt_data['private'] else self.public_path
            category = prompt_data['category'].lower().replace(' ', '_')
            save_path = os.path.join(base_location, category)
            
            # Create category directory
            ensure_directory_exists(save_path)
            
            # Generate filename
            filename = generate_safe_filename(prompt_data['title'], prompt_data['id'][:8])
            filepath = os.path.join(save_path, filename)
            
            # Save file
            if save_prompt_to_file(prompt_data, filepath):
                privacy_label = "Private" if prompt_data['private'] else "Public"
                print(f"\n📁 {privacy_label} prompt saved: {filepath}")
                return True
            
            return False
            
        except Exception as e:
            print_status(f"Error saving prompt: {e}", "error")
            return False
    
    def list_prompts(self):
        """List all available prompts"""
        display_header("Prompt Library")
        
        prompts = find_all_prompts(self.base_path)
        
        if not prompts:
            print_status("No prompts found", "warning")
            return
        
        # Group by privacy and category
        public_prompts = [p for p in prompts if not p.get('private', False)]
        private_prompts = [p for p in prompts if p.get('private', False)]
        
        if public_prompts:
            display_section(f"Public Prompts ({len(public_prompts)})")
            self._display_prompt_list(public_prompts)
        
        if private_prompts:
            display_section(f"Private Prompts ({len(private_prompts)})")
            self._display_prompt_list(private_prompts)
    
    def _display_prompt_list(self, prompts):
        """Display a list of prompts in table format"""
        if not prompts:
            print_status("No prompts found", "info")
            return
        
        # Prepare table data
        headers = ["#", "Title", "Category", "LLM", "Tags"]
        rows = []
        
        for i, prompt in enumerate(prompts, 1):
            title = prompt.get('title', 'Untitled')[:30]  # Truncate long titles
            category = prompt.get('category', 'general')[:20]
            
            # Get LLM recommendation - handle None values properly
            tech = prompt.get('technical_notes', {})
            if tech and isinstance(tech, dict):
                llm_raw = tech.get('recommended_llm')
                llm = (llm_raw or 'Not specified')[:15]
            else:
                llm = 'Not specified'
            
            # Get tags - handle None values properly
            tags = prompt.get('tags', [])
            if tags and isinstance(tags, list):
                tags_str = ', '.join(str(tag) for tag in tags)[:25]
            else:
                tags_str = 'None'
            
            rows.append([str(i), title, category, llm, tags_str])
        
        display_table(headers, rows)
        
        # Offer detailed view option
        print("💡 Enter a number (1-{}) to see detailed view, or press Enter to continue".format(len(prompts)))
        choice = input("Selection: ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(prompts):
                self._show_detailed_prompt(prompts[idx])
    
    def _show_detailed_prompt(self, prompt_data):
        """Show detailed view of a specific prompt"""
        display_section("Detailed Prompt View")
        display_prompt_summary(prompt_data)
        
        # Show AI analysis if available
        ai_analysis = prompt_data.get('ai_analysis', {})
        if ai_analysis:
            print("🤖 AI Analysis:")
            if ai_analysis.get('complexity_level'):
                print(f"   • Complexity: {ai_analysis['complexity_level']}")
            if ai_analysis.get('privacy_reasoning'):
                print(f"   • Privacy reasoning: {ai_analysis['privacy_reasoning']}")
            print()
        
        # Options for this prompt
        print("Actions:")
        print("[1] Copy content to clipboard")
        print("[2] Show full content")
        print("[3] Edit metadata")
        print("[4] Change privacy setting")
        print("[5] Delete prompt")
        print("[6] Back to list")
        
        options = ['Copy to clipboard', 'Show full content', 'Edit metadata', 'Change privacy setting', 'Delete prompt', 'Back to list']
        choice = get_user_choice(options, "Select action")
        
        if choice == 0:  # Copy to clipboard
            self._copy_to_clipboard(prompt_data['content'])
        elif choice == 1:  # Show full content
            self._show_full_content(prompt_data)
        elif choice == 2:  # Edit metadata
            print_status("Metadata editing coming soon", "info")
        elif choice == 3:  # Change privacy setting
            self._change_privacy_setting(prompt_data)
        elif choice == 4:  # Delete prompt
            self._delete_prompt(prompt_data)
        # choice == 5 returns to list
    
    def _copy_to_clipboard(self, content):
        """Copy content to clipboard if possible"""
        try:
            import pyperclip
            pyperclip.copy(content)
            print_status("Content copied to clipboard!", "success")
        except ImportError:
            print_status("Clipboard functionality requires 'pyperclip' package", "warning")
            print("Install with: pip install pyperclip")
            print("\nContent to copy:")
            print("-" * 50)
            print(content)
            print("-" * 50)
    
    def _show_full_content(self, prompt_data):
        """Show the full prompt content"""
        display_section(f"Full Content: {prompt_data['title']}")
        print(prompt_data['content'])
        print("\n" + "="*60)
        input("Press Enter to continue...")
    
    def _delete_prompt(self, prompt_data):
        """Delete a prompt with confirmation"""
        title = prompt_data.get('title', 'Unknown')
        
        if confirm_action(f"Are you sure you want to delete '{title}'?", default="n"):
            # Find and delete the file
            filepath = prompt_data.get('_filepath')
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
        title = prompt_data.get('title', 'Unknown')
        current_privacy = 'Private' if prompt_data.get('private', False) else 'Public'
        new_privacy = 'Public' if current_privacy == 'Private' else 'Private'
        
        display_section(f"Change Privacy: {title}")
        print(f"Current setting: {current_privacy}")
        print(f"New setting: {new_privacy}")
        
        # Show privacy implications
        if new_privacy == 'Private':
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
        
        if confirm_action(f"Change '{title}' from {current_privacy} to {new_privacy}?", default="n"):
            success = self._move_prompt_privacy(prompt_data, new_privacy == 'Private')
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
            current_filepath = prompt_data.get('_filepath')
            if not current_filepath or not os.path.exists(current_filepath):
                print_status("Cannot locate current prompt file", "error")
                return False
            
            # Update privacy setting in data
            prompt_data['private'] = make_private
            
            # Determine new location
            base_location = self.private_path if make_private else self.public_path
            category = prompt_data.get('category', 'general').lower().replace(' ', '_')
            new_directory = os.path.join(base_location, category)
            
            # Create new directory if needed
            ensure_directory_exists(new_directory)
            
            # Generate new filename (keep same ID)
            title = prompt_data.get('title', 'untitled')
            prompt_id = prompt_data.get('id', 'unknown')[:8]
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
        """Search prompts by title, content, category, or tags"""
        display_header("Search Prompts")
        
        search_query = input("Enter search term (title, category, content, or tag): ").strip().lower()
        
        if not search_query:
            print_status("No search term provided", "warning")
            return
        
        print_status(f"Searching for: '{search_query}'", "processing")
        
        # Get all prompts
        all_prompts = find_all_prompts(self.base_path)
        
        if not all_prompts:
            print_status("No prompts found in library", "warning")
            return
        
        # Search through prompts
        matches = []
        
        for prompt in all_prompts:
            # Search in title
            if search_query in prompt.get('title', '').lower():
                matches.append((prompt, 'title'))
                continue
            
            # Search in category
            if search_query in prompt.get('category', '').lower():
                matches.append((prompt, 'category'))
                continue
            
            # Search in tags
            tags = prompt.get('tags', [])
            if any(search_query in tag.lower() for tag in tags):
                matches.append((prompt, 'tags'))
                continue
            
            # Search in content (limited to first 500 chars for performance)
            content_preview = prompt.get('content', '')[:500].lower()
            if search_query in content_preview:
                matches.append((prompt, 'content'))
                continue
        
        if not matches:
            print_status(f"No matches found for '{search_query}'", "warning")
            return
        
        print_status(f"Found {len(matches)} match{'es' if len(matches) != 1 else ''}", "success")
        
        # Display results with match context
        display_section("Search Results")
        
        headers = ["#", "Title", "Category", "Match Type", "Privacy"]
        rows = []
        
        for i, (prompt, match_type) in enumerate(matches, 1):
            title = prompt.get('title', 'Untitled')[:25]
            category = prompt.get('category', 'general')[:15]
            privacy = 'Private' if prompt.get('private', False) else 'Public'
            
            rows.append([str(i), title, category, match_type.title(), privacy])
        
        display_table(headers, rows)
        
        # Offer detailed view option
        print("💡 Enter a number (1-{}) to see detailed view, or press Enter to continue".format(len(matches)))
        choice = input("Selection: ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                self._show_detailed_prompt(matches[idx][0])

def main():
    """Main application entry point"""
    manager = PromptManager()
    
    display_header("AI Prompt Manager V2")
    print("Streamlined prompt storage with intelligent metadata extraction")
    
    while True:
        print("\nOptions:")
        print("[1] Add new prompt")
        print("[2] List all prompts")
        print("[3] Search prompts")
        print("[4] Exit")
        
        try:
            choice = input("\nSelect option [1-4]: ").strip()
            
            if choice == '1':
                manager.add_prompt()
            elif choice == '2':
                manager.list_prompts()
            elif choice == '3':
                manager.search_prompts()
            elif choice == '4':
                print_status("Goodbye!", "success")
                break
            else:
                print_status("Invalid choice. Please select 1-4.", "error")
                
        except KeyboardInterrupt:
            print_status("\nGoodbye!", "success")
            break

if __name__ == "__main__":
    main()
