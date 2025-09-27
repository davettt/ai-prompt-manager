#!/usr/bin/env python3
"""
AI Prompt Manager - Main Entry Point
Professional prompt storage and retrieval system with intelligent metadata extraction

Usage:
    python main.py          # Interactive menu
    python test_system.py   # Run system tests
"""

import sys
import os
from utils.cli_helpers import print_status, print_header

def check_environment():
    """Check if the environment is properly configured"""
    issues = []
    
    # Check for .env file
    if not os.path.exists('.env'):
        issues.append("Missing .env file - copy from .env.example and add your API key")
    
    # Check for required directories
    if not os.path.exists('prompts'):
        print_status("Creating prompts directory structure...", "info")
        os.makedirs('prompts/public', exist_ok=True)
        os.makedirs('prompts/private', exist_ok=True)
    
    # Check dependencies
    try:
        import requests
        from dotenv import load_dotenv
    except ImportError as e:
        issues.append(f"Missing dependencies: {e}. Run 'pip install -r requirements.txt'")
    
    if issues:
        print_status("Environment issues detected:", "warning")
        for issue in issues:
            print(f"  • {issue}")
        print("\nℹ️  See USER_START.md for setup instructions")
        return False
    
    return True

def main():
    """Main application entry point with enhanced error handling"""
    try:
        print_header("AI Prompt Manager", "Professional prompt storage with intelligent metadata extraction")
        
        # Environment check
        if not check_environment():
            print_status("Please fix environment issues before continuing", "error")
            sys.exit(1)
        
        # Import and run prompt manager
        from prompt_manager import PromptManager
        
        manager = PromptManager()
        
        while True:
            print("\nOptions:")
            print("[1] Add new prompt")
            print("[2] List all prompts") 
            print("[3] Search prompts")
            print("[4] Run system tests")
            print("[5] Exit")
            
            try:
                choice = input("\nSelect option [1-5]: ").strip()
                
                if choice == '1':
                    manager.add_prompt()
                elif choice == '2':
                    manager.list_prompts()
                elif choice == '3':
                    manager.search_prompts()
                elif choice == '4':
                    print_status("Running system tests...", "info")
                    from test_system import run_all_tests
                    run_all_tests()
                elif choice == '5':
                    print_status("Thanks for using AI Prompt Manager! 👋", "success")
                    break
                else:
                    print_status("Invalid choice. Please select 1-5.", "error")
                    
            except KeyboardInterrupt:
                print_status("\n\nThanks for using AI Prompt Manager! 👋", "success")
                break
            except Exception as e:
                print_status(f"Unexpected error: {e}", "error")
                print("ℹ️  If this persists, please report the issue on GitHub")
                
    except ImportError as e:
        print_status(f"Import error: {e}", "error")
        print("ℹ️  Run 'pip install -r requirements.txt' to install dependencies")
        sys.exit(1)
    except Exception as e:
        print_status(f"Critical error: {e}", "error")
        print("ℹ️  Please check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
