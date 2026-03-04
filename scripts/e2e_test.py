#!/usr/bin/env python3
"""End-to-end test for SupportLens API. Verifies data flow and category filtering."""

import json
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import quote

def request(method: str, url: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method=method)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"

    # Health check
    health = request("GET", f"{base}/health")
    assert "status" in health, f"Invalid health: {health}"
    print(f"Health status: {health['status']}")

    # Initial analytics
    analytics_before = request("GET", f"{base}/analytics")
    total_before = analytics_before["total_traces"]
    print(f"Initial total traces: {total_before}")

    # Create trace (works without API key - classification defaults to General Inquiry)
    unique_msg = f"e2e-test-{int(time.time())}"
    trace = request("POST", f"{base}/traces", {
        "user_message": unique_msg,
        "bot_response": "E2E test response.",
        "response_time_ms": 100,
    })
    trace_id = trace["id"]
    print(f"Created trace: {trace_id}")

    # Verify analytics incremented
    analytics_after = request("GET", f"{base}/analytics")
    total_after = analytics_after["total_traces"]
    assert total_after == total_before + 1, f"Expected total {total_before + 1}, got {total_after}"
    print("Analytics increment verified.")

    # Verify trace in General Inquiry filter
    general = request("GET", f"{base}/traces?category={quote('General Inquiry')}")
    found = any(t["user_message"] == unique_msg for t in general)
    assert found, f"Trace not in General Inquiry filter"
    print("Category filter (General Inquiry) verified.")

    # Verify trace NOT in Billing filter
    billing = request("GET", f"{base}/traces?category=Billing")
    found_billing = any(t["user_message"] == unique_msg for t in billing)
    assert not found_billing, "Trace incorrectly in Billing filter"
    print("Category filter (Billing exclusion) verified.")

    print("=== E2E Test PASSED ===")

if __name__ == "__main__":
    main()
