#!/usr/bin/env python3
"""
AI Prompt Manager - System Test
Basic functionality testing for the prompt management system
"""

import os
import tempfile
import shutil
from datetime import datetime
from utils.cli_helpers import print_status, print_header
from metadata_extractor import extract_all_metadata
from prompt_manager import PromptManager

def test_metadata_extraction():
    """Test the metadata extraction functionality"""
    print_header("Testing Metadata Extraction")
    
    # Test prompt
    test_prompt = """# Elite Strategic Performance Advisor

**Recommended LLM**: Claude 3.5 Sonnet  
**Temperature**: 0.4  
**Max Tokens**: 4000-6000

You are an elite strategic performance advisor with deep expertise in systems thinking, evidence-based optimization, and high-performance psychology. Your role is to provide strategic guidance that accelerates performance through systematic approaches."""
    
    print("🧪 Testing with Elite Strategic Performance Advisor prompt...")
    
    try:
        metadata = extract_all_metadata(test_prompt)
        
        print_status("Metadata extraction completed", "success")
        print(f"Title: {metadata.get('title', 'Not detected')}")
        print(f"LLM: {metadata.get('recommended_llm', 'Not detected')}")
        print(f"Temperature: {metadata.get('temperature', 'Not detected')}")
        print(f"Max Tokens: {metadata.get('max_tokens', 'Not detected')}")
        print(f"Category: {metadata.get('ai_suggested_category', 'Not detected')}")
        print(f"Privacy: {metadata.get('ai_privacy_recommendation', 'Not detected')}")
        
        return True
        
    except Exception as e:
        print_status(f"Metadata extraction failed: {e}", "error")
        return False

def test_file_operations():
    """Test file operations"""
    print_header("Testing File Operations")
    
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        print(f"📁 Created temp directory: {temp_dir}")
        
        # Test prompt manager initialization
        manager = PromptManager(temp_dir)
        print_status("PromptManager initialized", "success")
        
        # Check directories were created
        public_path = os.path.join(temp_dir, "public")
        private_path = os.path.join(temp_dir, "private")
        
        if os.path.exists(public_path) and os.path.exists(private_path):
            print_status("Directory structure created correctly", "success")
        else:
            print_status("Directory structure creation failed", "error")
            return False
        
        # Cleanup
        shutil.rmtree(temp_dir)
        print_status("Cleanup completed", "success")
        
        return True
        
    except Exception as e:
        print_status(f"File operations test failed: {e}", "error")
        return False

def test_environment():
    """Test environment configuration"""
    print_header("Testing Environment")
    
    # Check for .env file
    if os.path.exists('.env'):
        print_status(".env file found", "success")
    else:
        print_status(".env file not found - create from .env.example", "warning")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print_status("ANTHROPIC_API_KEY configured", "success")
    else:
        print_status("ANTHROPIC_API_KEY not configured", "warning")
        print("ℹ️  Add your API key to .env file to test Claude integration")
    
    return True

def run_all_tests():
    """Run all system tests"""
    print_header("AI Prompt Manager - System Tests")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Environment Configuration", test_environment),
        ("File Operations", test_file_operations),
        ("Metadata Extraction", test_metadata_extraction),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
            status = "PASSED" if result else "FAILED"
            print_status(f"{test_name}: {status}", "success" if result else "error")
        except Exception as e:
            print_status(f"{test_name}: FAILED - {e}", "error")
            results.append((test_name, False))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    if passed == total:
        print_status("All tests passed! System is ready to use.", "success")
    else:
        print_status(f"{total - passed} test(s) failed. Check configuration.", "warning")

if __name__ == "__main__":
    run_all_tests()
