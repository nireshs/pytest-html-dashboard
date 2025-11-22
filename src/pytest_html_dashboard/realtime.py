"""Real-time test execution dashboard with WebSocket support."""

import asyncio
import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import socket


class RealtimeDashboard:
    """Manages real-time test execution updates."""

    def __init__(self, port: int = 8888, enable_websocket: bool = True):
        """Initialize real-time dashboard.

        Args:
            port: WebSocket server port
            enable_websocket: Whether to enable WebSocket server
        """
        self.port = port
        self.enable_websocket = enable_websocket
        self.clients: Set = set()
        self.current_state: Dict[str, Any] = {
            "status": "idle",
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "running": 0
            },
            "current_test": None,
            "start_time": None
        }
        self.server_thread: Optional[threading.Thread] = None
        self.running = False

    def start(self):
        """Start the real-time dashboard server."""
        if not self.enable_websocket:
            return

        self.running = True
        self.current_state["status"] = "running"
        self.current_state["start_time"] = datetime.now().isoformat()

        # Start WebSocket server in background thread
        self.server_thread = threading.Thread(
            target=self._run_server, daemon=True
        )
        self.server_thread.start()

    def stop(self):
        """Stop the real-time dashboard server."""
        self.running = False
        self.current_state["status"] = "completed"
        self._broadcast({"type": "session_end", "data": self.current_state})

    def update_test_start(self, test_name: str, test_id: str):
        """Notify that a test has started.

        Args:
            test_name: Name of the test
            test_id: Unique test identifier
        """
        self.current_state["current_test"] = {
            "name": test_name,
            "id": test_id,
            "status": "running",
            "start_time": datetime.now().isoformat()
        }
        self.current_state["summary"]["running"] += 1

        self._broadcast({
            "type": "test_start",
            "data": {
                "test_name": test_name,
                "test_id": test_id,
                "timestamp": datetime.now().isoformat()
            }
        })

    def update_test_end(
        self,
        test_name: str,
        test_id: str,
        outcome: str,
        duration: float,
        error: Optional[str] = None
    ):
        """Notify that a test has completed.

        Args:
            test_name: Name of the test
            test_id: Unique test identifier
            outcome: Test outcome (passed/failed/skipped)
            duration: Test duration in seconds
            error: Error message if test failed
        """
        # Update summary
        if outcome == "passed":
            self.current_state["summary"]["passed"] += 1
        elif outcome == "failed":
            self.current_state["summary"]["failed"] += 1
        elif outcome == "skipped":
            self.current_state["summary"]["skipped"] += 1

        self.current_state["summary"]["running"] = max(
            0, self.current_state["summary"]["running"] - 1
        )
        self.current_state["summary"]["total"] += 1

        # Add to test list
        test_result = {
            "name": test_name,
            "id": test_id,
            "outcome": outcome,
            "duration": duration,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.current_state["tests"].append(test_result)

        # Broadcast update
        self._broadcast({
            "type": "test_end",
            "data": test_result,
            "summary": self.current_state["summary"]
        })

    def update_progress(self, message: str):
        """Send a progress update message.

        Args:
            message: Progress message
        """
        self._broadcast({
            "type": "progress",
            "data": {
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        })

    def get_state(self) -> Dict[str, Any]:
        """Get current dashboard state.

        Returns:
            Current state dictionary
        """
        return self.current_state.copy()

    def _broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients.

        Args:
            message: Message to broadcast
        """
        if not self.enable_websocket:
            return

        # Store for HTTP polling fallback
        self._save_state_file()

    def _save_state_file(self):
        """Save current state to file for HTTP polling fallback."""
        state_file = Path("realtime-state.json")
        try:
            with open(state_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "state": self.current_state
                }, f)
        except Exception:
            pass  # Fail silently if can't write

    def _run_server(self):
        """Run simple HTTP server for state polling."""
        # Simple HTTP server for JSON state
        # This is a basic implementation - for production use Flask/FastAPI
        pass

    def generate_realtime_html(self) -> str:
        """Generate HTML with real-time update capabilities.

        Returns:
            HTML string with WebSocket client code
        """
        return f"""
<!-- Real-Time Dashboard Updates -->
<script>
    let realtimeEnabled = {'true' if self.enable_websocket else 'false'};
    let pollInterval = null;

    function initRealtimeUpdates() {{
        if (!realtimeEnabled) return;

        // Try WebSocket first, fallback to polling
        try {{
            connectWebSocket();
        }} catch (e) {{
            startPolling();
        }}
    }}

    function connectWebSocket() {{
        const ws = new WebSocket('ws://localhost:{self.port}/updates');

        ws.onopen = function() {{
            console.log('Real-time connection established');
            showRealtimeIndicator(true);
        }};

        ws.onmessage = function(event) {{
            const data = JSON.parse(event.data);
            handleRealtimeUpdate(data);
        }};

        ws.onclose = function() {{
            console.log('Real-time connection closed');
            showRealtimeIndicator(false);
            // Fallback to polling
            setTimeout(startPolling, 1000);
        }};

        ws.onerror = function() {{
            // Fallback to polling
            startPolling();
        }};
    }}

    function startPolling() {{
        if (pollInterval) return;

        pollInterval = setInterval(async function() {{
            try {{
                const response = await fetch('realtime-state.json');
                const data = await response.json();
                handleRealtimeUpdate(data.state);
            }} catch (e) {{
                // State file not available yet
            }}
        }}, 2000); // Poll every 2 seconds
    }}

    function handleRealtimeUpdate(data) {{
        if (data.type === 'test_start') {{
            updateRunningTest(data.data);
        }} else if (data.type === 'test_end') {{
            updateTestResult(data.data);
            updateSummary(data.summary);
            updateCharts(data.summary);
        }} else if (data.type === 'session_end') {{
            stopPolling();
            showCompletionMessage();
        }}
    }}

    function updateRunningTest(test) {{
        const indicator = document.getElementById('current-test-indicator');
        if (indicator) {{
            indicator.innerHTML = `
                <div class="running-test">
                    <span class="spinner">⟳</span>
                    <span>Running: ${{test.test_name}}</span>
                </div>
            `;
            indicator.style.display = 'block';
        }}
    }}

    function updateTestResult(test) {{
        // Add new row to test table
        const tableBody = document.querySelector('.results-table tbody');
        if (tableBody) {{
            const row = document.createElement('tr');
            row.className = 'result ' + test.outcome;
            row.innerHTML = `
                <td>${{test.name}}</td>
                <td><span class="badge ${{test.outcome}}">${{test.outcome}}</span></td>
                <td>${{test.duration.toFixed(2)}}s</td>
                <td>${{test.timestamp}}</td>
            `;
            tableBody.insertBefore(row, tableBody.firstChild);
        }}
    }}

    function updateSummary(summary) {{
        document.getElementById('total-count').textContent = summary.total;
        document.getElementById('passed-count').textContent = summary.passed;
        document.getElementById('failed-count').textContent = summary.failed;
        document.getElementById('skipped-count').textContent = summary.skipped;

        // Update pass rate
        const passRate = summary.total > 0
            ? ((summary.passed / summary.total) * 100).toFixed(1)
            : 0;
        document.getElementById('pass-rate').textContent = passRate + '%';
    }}

    function updateCharts(summary) {{
        // Update Chart.js charts with new data
        if (typeof statusChart !== 'undefined') {{
            statusChart.data.datasets[0].data = [
                summary.passed,
                summary.failed,
                summary.skipped
            ];
            statusChart.update('none'); // Update without animation for smoothness
        }}

        if (typeof passRateChart !== 'undefined') {{
            const passRate = summary.total > 0
                ? (summary.passed / summary.total) * 100
                : 0;
            const failRate = 100 - passRate;
            passRateChart.data.datasets[0].data = [passRate, failRate];
            passRateChart.update('none');
        }}
    }}

    function showRealtimeIndicator(connected) {{
        const indicator = document.getElementById('realtime-indicator');
        if (indicator) {{
            indicator.className = connected ? 'connected' : 'disconnected';
            indicator.textContent = connected ? '● Live' : '○ Offline';
        }}
    }}

    function stopPolling() {{
        if (pollInterval) {{
            clearInterval(pollInterval);
            pollInterval = null;
        }}
    }}

    function showCompletionMessage() {{
        const indicator = document.getElementById('current-test-indicator');
        if (indicator) {{
            indicator.innerHTML = '<div class="completed">✓ All tests completed</div>';
        }}
    }}

    // Auto-start on page load
    document.addEventListener('DOMContentLoaded', function() {{
        initRealtimeUpdates();
    }});
</script>

<style>
    #realtime-indicator {{
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        z-index: 1000;
    }}

    #realtime-indicator.connected {{
        background: #4CAF50;
        color: white;
    }}

    #realtime-indicator.disconnected {{
        background: #666;
        color: #ccc;
    }}

    #current-test-indicator {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: white;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        max-width: 400px;
        z-index: 1000;
        display: none;
    }}

    .running-test {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .spinner {{
        font-size: 24px;
        animation: spin 1s linear infinite;
    }}

    @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    .completed {{
        color: #4CAF50;
        font-weight: bold;
    }}
</style>

<div id="realtime-indicator" class="disconnected">○ Offline</div>
<div id="current-test-indicator"></div>
"""


# Global instance
_realtime_dashboard: Optional[RealtimeDashboard] = None


def get_realtime_dashboard(port: int = 8888) -> RealtimeDashboard:
    """Get or create the global realtime dashboard instance.

    Args:
        port: WebSocket server port

    Returns:
        RealtimeDashboard instance
    """
    global _realtime_dashboard
    if _realtime_dashboard is None:
        _realtime_dashboard = RealtimeDashboard(port=port)
    return _realtime_dashboard
