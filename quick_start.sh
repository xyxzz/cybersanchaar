#!/bin/bash

# Quick Start Script for Cybersecurity News App
# This script helps you get started quickly

echo "🔒 Cybersecurity News Application - Quick Start"
echo "=============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed"
    exit 1
fi

echo "✅ pip found"

# Create virtual environment
echo ""
echo "🐍 Creating virtual environment..."
python3 -m venv news

echo "✅ Virtual environment created"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
source news/bin/activate && pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo ""
echo "📁 Setting up directories..."
mkdir -p data cache logs

echo "✅ Directories created"

# Show available commands
echo ""
echo "🚀 Setup complete! Here are some commands to get started:"
echo ""
echo "# First, always activate the virtual environment:"
echo "source news/bin/activate"
echo ""
echo "# Update news from all sources:"
echo "python cyber_news_app.py --update"
echo ""
echo "# Show today's news:"
echo "python cyber_news_app.py"
echo ""
echo "# Start web interface:"
echo "python cyber_news_app.py --web"
echo ""
echo "# Show all available options:"
echo "python cyber_news_app.py --help"
echo ""
echo "# List configured sources:"
echo "python cyber_news_app.py --sources-list"
echo ""

# Ask if user wants to fetch news now
echo -n "Would you like to fetch the latest news now? (y/n): "
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 Fetching latest cybersecurity news..."
    source news/bin/activate && python cyber_news_app.py --update
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "📰 Displaying today's news:"
        source news/bin/activate && python cyber_news_app.py
    else
        echo "❌ Failed to update news. Check the logs for details."
    fi
fi

echo ""
echo "🎉 Quick start completed! Enjoy staying informed about cybersecurity news."