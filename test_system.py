#!/usr/bin/env python3
"""
Test script for AI Prompt Manager V2
Quick validation of core functionality
"""

import os
import sys

def test_imports():
    """Test that all modules can be imported"""
    try:
        from prompt_manager import PromptManager
        from metadata_extractor import extract_all_metadata
        from utils.cli_helpers import print_status
        from utils.file_helpers import ensure_directory_exists
        
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    required_dirs = ['prompts', 'prompts/public', 'prompts/private']
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Missing directory: {dir_path}")
            return False
    
    print("✅ All required directories exist")
    return True

def test_env_file():
    """Test that .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found - Claude API features will not work")
        return False
    
    print("✅ .env file exists")
    return True

def test_metadata_extraction():
    """Test metadata extraction with sample content"""
    try:
        from metadata_extractor import extract_title, extract_technical_notes
        
        test_content = """# Test Prompt

**Recommended LLM**: Claude 3.5 Sonnet | **Temperature**: 0.4 | **Max Tokens**: 1000

You are a helpful assistant."""
        
        title = extract_title(test_content)
        tech_notes = extract_technical_notes(test_content)
        
        if title == "Test Prompt":
            print("✅ Title extraction working")
        else:
            print(f"❌ Title extraction failed: got '{title}' expected 'Test Prompt'")
            return False
        
        if tech_notes['recommended_llm'] == 'Claude 3.5 Sonnet':
            print("✅ Technical notes extraction working")
        else:
            print(f"❌ Tech extraction failed: got '{tech_notes['recommended_llm']}'")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Metadata extraction error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Prompt Manager V2 - System Test")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Directory Structure", test_directories), 
        ("Environment File", test_env_file),
        ("Metadata Extraction", test_metadata_extraction)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        if test_func():
            passed += 1
    
    print(f"\n{'=' * 40}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems ready! You can run: python main.py")
    else:
        print("⚠️  Some issues found. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
