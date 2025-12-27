#!/bin/bash
# Fix Tailwind CSS v4 -> v3 for Next.js compatibility

echo "🔧 Fixing Tailwind CSS Configuration..."
echo "========================================"

cd frontend

# Stop any running Next.js process
echo "📛 Stopping Next.js..."
pkill -f "next dev" 2>/dev/null || true
sleep 2

# Remove Tailwind v4 packages
echo "🗑️  Removing Tailwind CSS v4..."
npm uninstall tailwindcss @tailwindcss/postcss

# Install Tailwind v3 (stable)
echo "📥 Installing Tailwind CSS v3..."
npm install -D tailwindcss@^3.4.0 postcss@^8.4.0 autoprefixer@^10.4.0

# Clear caches
echo "🧹 Clearing caches..."
rm -rf .next node_modules/.cache

echo ""
echo "✅ Tailwind CSS fixed!"
echo ""
echo "Now restart the frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Or use the startup script:"
echo "  ./start-frontend.sh"


