#!/usr/bin/env python3
"""
Demo script showing key features of the Cybersecurity News Application
Run this to see the application in action
"""

import subprocess
import sys
import time

def run_command(cmd, description):
    """Run a command and display its output"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print('='*60)
    
    try:
        # Activate virtual environment and run command
        full_cmd = f"bash -c 'source news/bin/activate && {cmd}'"
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"Error running command: {e}")
    
    print("\nPress Enter to continue...")
    input()

def main():
    """Main demo function"""
    print("🔒 Cybersecurity News Application - DEMO")
    print("=======================================")
    print("This demo will show you the key features of the application.")
    print("Make sure you've run the quick_start.sh script first!")
    print("\nPress Enter to start the demo...")
    input()
    
    # Demo commands
    demos = [
        ("python cyber_news_app.py --help", "Command line help and options"),
        ("python cyber_news_app.py --sources-list", "Configured news sources"),
        ("python cyber_news_app.py --update", "Fetching latest cybersecurity news"),
        ("python cyber_news_app.py --show --days 1", "Displaying today's top news"),
        ("python cyber_news_app.py --show --categories threats --days 2", "Filtering by threat category"),
        ("python cyber_news_app.py --stats", "News statistics and analytics"),
        ("python cyber_news_app.py --export json --days 1", "Exporting news to JSON format"),
    ]
    
    for cmd, description in demos:
        run_command(cmd, description)
    
    print("\n🎉 Demo completed!")
    print("\nNext steps:")
    print("1. Run 'python cyber_news_app.py --web' to start the web interface")
    print("2. Run 'python cyber_news_app.py --daemon' for scheduled updates")
    print("3. Customize config.yaml for your specific needs")
    print("4. Set up as a systemd service for production use")

if __name__ == "__main__":
    main()