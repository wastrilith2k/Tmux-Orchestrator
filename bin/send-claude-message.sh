#!/bin/bash

# Enhanced send-claude-message.sh v2.0
# Send message to Claude agent in tmux window with logging and validation
# Usage: send-claude-message.sh <session:window> <message>

# Get script directory for logging
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs/communications"
LOG_FILE="$LOG_DIR/messages-$(date +%Y%m%d).log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Function to log messages
log_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" >> "$LOG_FILE"
}

# Function to validate target exists
validate_target() {
    local target="$1"
    local session="${target%:*}"
    local window="${target#*:}"

    # Check if session exists
    if ! tmux has-session -t "$session" 2>/dev/null; then
        echo "ERROR: Session '$session' does not exist"
        log_message "ERROR: Failed to send to $target - session does not exist"
        echo "Available sessions:"
        tmux list-sessions 2>/dev/null || echo "No tmux sessions found"
        return 1
    fi

    # Check if window exists
    if ! tmux list-windows -t "$session" -F "#{window_index}" 2>/dev/null | grep -q "^${window}$"; then
        echo "ERROR: Window '$window' does not exist in session '$session'"
        log_message "ERROR: Failed to send to $target - window does not exist"
        echo "Available windows in session '$session':"
        tmux list-windows -t "$session" -F "#{window_index}: #{window_name}" 2>/dev/null
        return 1
    fi

    return 0
}

if [ $# -lt 2 ]; then
    echo "Usage: $0 <session:window> <message>"
    echo "Example: $0 agentic-seek:3 'Hello Claude!'"
    log_message "ERROR: Invalid usage - insufficient arguments"
    exit 1
fi

WINDOW="$1"
shift  # Remove first argument, rest is the message
MESSAGE="$*"

# Validate target before sending
if ! validate_target "$WINDOW"; then
    exit 1
fi

# Log the attempt
log_message "SENDING to $WINDOW: $MESSAGE"

# Send the message
if tmux send-keys -t "$WINDOW" "$MESSAGE" 2>/dev/null; then
    # Wait 0.5 seconds for UI to register
    sleep 0.5

    # Send Enter to submit
    if tmux send-keys -t "$WINDOW" Enter 2>/dev/null; then
        echo "Message sent to $WINDOW: $MESSAGE"
        log_message "SUCCESS: Message sent to $WINDOW"
    else
        echo "ERROR: Failed to send Enter key to $WINDOW"
        log_message "ERROR: Failed to send Enter key to $WINDOW"
        exit 1
    fi
else
    echo "ERROR: Failed to send message to $WINDOW"
    log_message "ERROR: Failed to send message to $WINDOW"
    exit 1
fi