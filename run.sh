#!/bin/bash
set -e

echo "=== AI Resume Scanner Setup ==="

# Install dependencies
pip install -r requirements.txt -q
python -m spacy download en_core_web_sm -q 2>/dev/null || true

# Copy env if not exists
[ ! -f backend/.env ] && cp .env.example backend/.env && echo "Created backend/.env — add your JSEARCH_API_KEY for live jobs"

echo ""
echo "Starting Flask backend on http://127.0.0.1:5000 ..."
cd backend && python app.py &
BACKEND_PID=$!

sleep 2

echo "Opening frontend..."
# Try to open browser
if command -v xdg-open &>/dev/null; then
  xdg-open ../frontend/index.html
elif command -v open &>/dev/null; then
  open ../frontend/index.html
else
  echo "Open frontend/index.html in your browser manually."
fi

echo ""
echo "✅ Running! Press Ctrl+C to stop."
wait $BACKEND_PID
