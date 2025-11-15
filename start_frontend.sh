#!/bin/bash

# InvestBuddy Frontend Startup Script

echo "🎨 Starting InvestBuddy Frontend..."
echo "==================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Warning: Backend doesn't seem to be running on port 8000"
    echo "   Make sure to run ./start_backend.sh in another terminal first!"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to cancel..."
fi

echo ""
echo "🌐 Starting Streamlit frontend..."
echo "   Frontend will open automatically in your browser"
echo "   Press Ctrl+C to stop"
echo ""

streamlit run frontend.py
