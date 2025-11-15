#!/bin/bash

# InvestBuddy Backend Startup Script

echo "🚀 Starting InvestBuddy Backend..."
echo "=================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with OPENAI_API_KEY"
    exit 1
fi

# Start backend
echo "📡 Starting FastAPI server on http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""

uvicorn backend:app --reload
