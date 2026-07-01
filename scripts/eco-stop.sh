#!/bin/bash

echo "Stopping EcoVibe Concierge..."

# Forcefully kill all Python instances running on Windows to release locks
taskkill //F //IM python.exe //T 2>/dev/null || taskkill /F /IM python.exe /T 2>/dev/null

# Clean up any lingering processes holding port 8080 active
PID_ON_PORT=$(netstat -ano | grep :8080 | awk '{print $5}' | head -n 1 | tr -d '\r')

if [ -n "$PID_ON_PORT" ]; then
    echo "Found process $PID_ON_PORT holding port 8080. Terminating..."
    taskkill //F //PID "$PID_ON_PORT" 2>/dev/null || taskkill /F /PID "$PID_ON_PORT"
else
    echo "Port 8080 is clear."
fi

echo "✓ EcoVibe Concierge stopped successfully."



