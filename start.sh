#!/usr/bin/env bash
set -e

# ImplementAI Labs — Start automation server + tunnel

# 1. Load env vars if .env exists
if [ -f .env ]; then
    set -a; source .env; set +a
fi

PORT="${PORT:-5001}"

# 2. Start the Flask webhook server in background
echo "[START] Launching webhook server on port $PORT..."
python3 tally_flow_pro.py &
SERVER_PID=$!
echo "[OK] Server PID: $SERVER_PID"

# Give it a second to boot
sleep 2

# Check it's running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "[ERROR] Server failed to start"
    exit 1
fi

echo "[OK] Health check: $(curl -s http://localhost:$PORT/health)"

# 3. Start localtunnel
echo "[START] Opening localtunnel..."
npx localtunnel --port $PORT &
TUNNEL_PID=$!

echo ""
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║  Server running at http://localhost:$PORT       ║"
echo "  ║  Tunnel URL will appear above                    ║"
echo "  ║  Configure Tally webhook to:                    ║"
echo "  ║  https://<tunnel-url>/tally-webhook              ║"
echo "  ║                                               ║"
echo "  ║  Press Ctrl+C to stop.                         ║"
echo "  ╚══════════════════════════════════════════════╝"

# Wait for either process
wait
