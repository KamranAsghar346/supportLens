#!/usr/bin/env bash
# End-to-end test for SupportLens API.
# Verifies data flow: create trace -> analytics increment, category filter works.
# Runs without OPENAI_API_KEY (app degrades gracefully).

set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== E2E Test: SupportLens API ==="
echo "Backend URL: $BACKEND_URL"

# Wait for backend to be healthy
echo "Waiting for backend..."
for i in $(seq 1 30); do
    if curl -sf "$BACKEND_URL/health" > /dev/null 2>&1; then
        echo "Backend is up."
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "ERROR: Backend did not become healthy in time."
        exit 1
    fi
    sleep 2
done

python3 "$SCRIPT_DIR/e2e_test.py" "$BACKEND_URL"
