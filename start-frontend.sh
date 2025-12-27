#!/bin/bash
# Start the Next.js frontend server

echo "🚀 Starting Next.js Frontend..."
echo "================================"

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Installing dependencies..."
    npm install
fi

# Start the development server
echo "✅ Starting server on http://localhost:3000"
echo ""
npm run dev

