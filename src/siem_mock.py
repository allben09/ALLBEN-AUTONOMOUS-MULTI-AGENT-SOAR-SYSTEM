"""
src/siem_mock.py
Simulates Wazuh/Splunk alerts for testing.
"""
import random

def generate_mock_alert():
    alerts = [
        {
            "rule": "SSH Bruteforce",
            "source_ip": "185.220.101.5",
            "user": "root",
            "attempts": 154
        },
        {
            "rule": "Port Scan Detected",
            "source_ip": "8.8.8.8",
            "target_port": 443
        },
        {
            "rule": "SQL Injection Attempt",
            "source_ip": "45.142.212.61",
            "target": "/api/v1/login"
        }
    ]
    return random.choice(alerts)
