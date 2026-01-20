#!/bin/bash
# Promotion Hub - Start Script for Linux/Mac
# Run this to start the automation system

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   PROMOTION HUB - Starting...           ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9+ using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3.9"
    echo "  macOS: brew install python3"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    echo "Please copy .env.example to .env and fill in your credentials:"
    echo "  cp .env.example .env"
    exit 1
fi

# Run system check first
echo "Running pre-flight checks..."
python3 system_check.py
if [ $? -ne 0 ]; then
    echo ""
    echo "Pre-flight checks failed. Please fix errors above."
    exit 1
fi

# Run main application
echo ""
echo "Starting Promotion Hub..."
echo ""
python3 main.py

# If we get here, app exited
echo ""
echo "Application exited. Check logs/promotion_hub.log for details."
