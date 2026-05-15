#!/bin/bash
cd "$(dirname "$0")"
echo "Starting NewsHour Flock API Server..."
echo "Leave this running. Admin button on website needs this."
echo ""
python3 server.py
