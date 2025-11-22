"""Historical test results tracking and trend analysis."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib


class TestHistory:
    """Manages historical test result data storage and retrieval."""

    def __init__(self, db_path: str = "test-history.db"):
        """Initialize the test history database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self._init_database()

    def _init_database(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Test runs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_runs (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_tests INTEGER,
                    passed INTEGER,
                    failed INTEGER,
                    skipped INTEGER,
                    errors INTEGER,
                    duration REAL,
                    branch TEXT,
                    commit_hash TEXT,
                    environment TEXT,
                    metadata TEXT
                )
            """)

            # Individual test results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER,
                    test_id TEXT,
                    test_name TEXT,
                    outcome TEXT,
                    duration REAL,
                    error_message TEXT,
                    error_type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (run_id) REFERENCES test_runs(run_id)
                )
            """)

            # Flaky tests tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flaky_tests (
                    test_id TEXT PRIMARY KEY,
                    test_name TEXT,
                    flaky_count INTEGER DEFAULT 1,
                    last_flip_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    pass_count INTEGER DEFAULT 0,
                    fail_count INTEGER DEFAULT 0
                )
            """)

            # Create indexes for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_test_results_run_id
                ON test_results(run_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_test_results_test_id
                ON test_results(test_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_test_runs_timestamp
                ON test_runs(timestamp)
            """)

            conn.commit()

    def _generate_test_id(self, test_name: str) -> str:
        """Generate a stable ID for a test based on its name.

        Args:
            test_name: Full test name including module and parameters

        Returns:
            Unique test identifier
        """
        return hashlib.md5(test_name.encode()).hexdigest()

    def save_test_run(
        self,
        results: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Save a complete test run to the database.

        Args:
            results: Test run results dictionary
            metadata: Optional metadata (branch, commit, etc.)

        Returns:
            The run_id of the saved test run
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Extract summary data
            summary = results.get('summary', {})
            metadata_dict = metadata or {}

            # Insert test run
            cursor.execute("""
                INSERT INTO test_runs
                (total_tests, passed, failed, skipped, errors, duration,
                 branch, commit_hash, environment, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary.get('total', 0),
                summary.get('passed', 0),
                summary.get('failed', 0),
                summary.get('skipped', 0),
                summary.get('errors', 0),
                summary.get('duration', 0.0),
                metadata_dict.get('branch'),
                metadata_dict.get('commit_hash'),
                metadata_dict.get('environment'),
                json.dumps(metadata_dict)
            ))

            run_id = cursor.lastrowid

            # Insert individual test results
            for test in results.get('tests', []):
                test_id = self._generate_test_id(test.get('name', ''))
                cursor.execute("""
                    INSERT INTO test_results
                    (run_id, test_id, test_name, outcome, duration,
                     error_message, error_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    run_id,
                    test_id,
                    test.get('name'),
                    test.get('outcome'),
                    test.get('duration', 0.0),
                    test.get('error_message'),
                    test.get('error_type')
                ))

                # Update flaky test tracking
                self._update_flaky_detection(
                    cursor, test_id, test.get('name'), test.get('outcome')
                )

            conn.commit()
            return run_id

    def _update_flaky_detection(
        self, cursor, test_id: str, test_name: str, outcome: str
    ):
        """Update flaky test detection based on test outcome.

        Args:
            cursor: Database cursor
            test_id: Test identifier
            test_name: Test name
            outcome: Test outcome (passed/failed)
        """
        # Get previous outcome
        cursor.execute("""
            SELECT outcome FROM test_results
            WHERE test_id = ?
            ORDER BY timestamp DESC LIMIT 1
        """, (test_id,))

        previous = cursor.fetchone()

        if previous and previous[0] != outcome:
            # Test outcome flipped - it's flaky
            cursor.execute("""
                INSERT INTO flaky_tests (test_id, test_name, flaky_count)
                VALUES (?, ?, 1)
                ON CONFLICT(test_id) DO UPDATE SET
                    flaky_count = flaky_count + 1,
                    last_flip_date = CURRENT_TIMESTAMP
            """, (test_id, test_name))

        # Update pass/fail counts
        if outcome == 'passed':
            cursor.execute("""
                INSERT INTO flaky_tests (test_id, test_name, pass_count)
                VALUES (?, ?, 1)
                ON CONFLICT(test_id) DO UPDATE SET
                    pass_count = pass_count + 1
            """, (test_id, test_name))
        elif outcome == 'failed':
            cursor.execute("""
                INSERT INTO flaky_tests (test_id, test_name, fail_count)
                VALUES (?, ?, 1)
                ON CONFLICT(test_id) DO UPDATE SET
                    fail_count = fail_count + 1
            """, (test_id, test_name))

    def get_trend_data(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get historical trend data for the last N runs.

        Args:
            limit: Number of recent runs to retrieve

        Returns:
            List of test run summaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT run_id, timestamp, total_tests, passed, failed,
                       skipped, errors, duration, branch
                FROM test_runs
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_flaky_tests(self, min_flips: int = 2) -> List[Dict[str, Any]]:
        """Get list of flaky tests.

        Args:
            min_flips: Minimum number of flips to consider a test flaky

        Returns:
            List of flaky test information
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT test_id, test_name, flaky_count, last_flip_date,
                       pass_count, fail_count
                FROM flaky_tests
                WHERE flaky_count >= ?
                ORDER BY flaky_count DESC
            """, (min_flips,))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_test_history(
        self, test_name: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get history for a specific test.

        Args:
            test_name: Name of the test
            limit: Number of recent results to retrieve

        Returns:
            List of test results over time
        """
        test_id = self._generate_test_id(test_name)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tr.timestamp, tr.outcome, tr.duration,
                       tr.error_message, tr.error_type
                FROM test_results tr
                WHERE tr.test_id = ?
                ORDER BY tr.timestamp DESC
                LIMIT ?
            """, (test_id, limit))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics from test history.

        Returns:
            Dictionary with various statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total runs
            cursor.execute("SELECT COUNT(*) FROM test_runs")
            total_runs = cursor.fetchone()[0]

            # Average pass rate
            cursor.execute("""
                SELECT AVG(CAST(passed AS FLOAT) / NULLIF(total_tests, 0) * 100)
                FROM test_runs
            """)
            avg_pass_rate = cursor.fetchone()[0] or 0

            # Most failed tests
            cursor.execute("""
                SELECT test_name, COUNT(*) as fail_count
                FROM test_results
                WHERE outcome = 'failed'
                GROUP BY test_name
                ORDER BY fail_count DESC
                LIMIT 5
            """)
            most_failed = [
                {"test_name": row[0], "fail_count": row[1]}
                for row in cursor.fetchall()
            ]

            # Slowest tests (average)
            cursor.execute("""
                SELECT test_name, AVG(duration) as avg_duration
                FROM test_results
                GROUP BY test_name
                ORDER BY avg_duration DESC
                LIMIT 5
            """)
            slowest_tests = [
                {"test_name": row[0], "avg_duration": row[1]}
                for row in cursor.fetchall()
            ]

            return {
                "total_runs": total_runs,
                "average_pass_rate": round(avg_pass_rate, 2),
                "most_failed_tests": most_failed,
                "slowest_tests": slowest_tests
            }

    def get_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get trend data for the dashboard.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend metrics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total runs
            cursor.execute("""
                SELECT COUNT(*) FROM test_runs
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
            """, (days,))
            total_runs = cursor.fetchone()[0]
            
            # Pass rate change
            cursor.execute("""
                SELECT 
                    AVG(CASE WHEN timestamp >= datetime('now', '-' || ? || ' days') 
                        THEN pass_rate ELSE NULL END) as recent,
                    AVG(CASE WHEN timestamp < datetime('now', '-' || ? || ' days') 
                        THEN pass_rate ELSE NULL END) as old
                FROM test_runs
            """, (days, days))
            row = cursor.fetchone()
            recent_rate = row[0] or 0
            old_rate = row[1] or recent_rate
            pass_rate_change = recent_rate - old_rate
            
            # Flaky tests count
            cursor.execute("SELECT COUNT(*) FROM flaky_tests")
            flaky_count = cursor.fetchone()[0]
            
            # Average duration
            cursor.execute("""
                SELECT AVG(duration) FROM test_results
                WHERE run_id IN (
                    SELECT run_id FROM test_runs
                    WHERE timestamp >= datetime('now', '-' || ? || ' days')
                )
            """, (days,))
            avg_duration = cursor.fetchone()[0] or 0.0
            
            return {
                "total_runs": total_runs,
                "pass_rate_change": round(pass_rate_change, 2),
                "flaky_tests": flaky_count,
                "avg_duration": round(avg_duration, 3)
            }

    def clear_old_data(self, days: int = 90):
        """Remove test data older than specified days.

        Args:
            days: Number of days to retain
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM test_results
                WHERE run_id IN (
                    SELECT run_id FROM test_runs
                    WHERE timestamp < datetime('now', '-' || ? || ' days')
                )
            """, (days,))

            cursor.execute("""
                DELETE FROM test_runs
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            """, (days,))

            conn.commit()
