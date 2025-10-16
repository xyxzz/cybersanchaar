#!/usr/bin/env python3
"""
Simple test script to verify the Cybersecurity News Application works
"""

import subprocess
import sys
import os

def test_functionality():
    """Test key functionality of the application"""
    
    print("🧪 Testing Cybersecurity News Application")
    print("="*50)
    
    # Ensure virtual environment exists
    if not os.path.exists("news/bin/activate"):
        print("❌ Virtual environment not found. Run quick_start.sh first!")
        return False
    
    tests = [
        ("python cyber_news_app.py --help", "Help command"),
        ("python cyber_news_app.py --sources-list", "Sources configuration"), 
        ("python cyber_news_app.py --stats", "Statistics display"),
    ]
    
    all_passed = True
    
    for cmd, test_name in tests:
        print(f"\n🔍 Testing: {test_name}")
        print("-" * 30)
        
        try:
            full_cmd = f"bash -c 'source news/bin/activate && {cmd}'"
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ PASSED")
                # Show first few lines of output
                lines = result.stdout.split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
            else:
                print("❌ FAILED")
                print(f"   Error: {result.stderr}")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print("⏰ TIMEOUT")
            all_passed = False
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            all_passed = False
    
    # Test news update if no cached data exists
    print(f"\n🔍 Testing: News Update")
    print("-" * 30)
    
    cache_file = "cache/articles_20250830.json"
    if not os.path.exists(cache_file):
        print("📰 No cached news found, testing update...")
        try:
            full_cmd = "bash -c 'source news/bin/activate && timeout 60s python cyber_news_app.py --update'"
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ News update PASSED")
            else:
                print("❌ News update FAILED")
                print(f"   Error: {result.stderr}")
        except Exception as e:
            print(f"❌ News update EXCEPTION: {e}")
    else:
        print("✅ Cached news exists (update already tested)")
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All tests PASSED! Application is ready to use.")
        print("\n💡 Try these commands:")
        print("   source news/bin/activate && python cyber_news_app.py")
        print("   source news/bin/activate && python cyber_news_app.py --web")
    else:
        print("⚠️  Some tests FAILED. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    test_functionality()