#!/bin/bash

# Agent Communication System for Tmux Orchestrator
# Handles message queuing and coordination between agents

COMM_DIR="/tmp/agent-communication"
mkdir -p "$COMM_DIR"

send_message() {
    local from_agent="$1"
    local to_agent="$2"
    local message="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Create message file
    local msg_file="$COMM_DIR/${to_agent}_inbox.txt"
    echo "[$timestamp] FROM $from_agent: $message" >> "$msg_file"

    echo "✉️ Message sent from $from_agent to $to_agent: $message"
}

read_messages() {
    local agent_name="$1"
    local inbox="$COMM_DIR/${agent_name}_inbox.txt"

    if [ -f "$inbox" ] && [ -s "$inbox" ]; then
        echo "📬 Messages for $agent_name:"
        cat "$inbox"
        # Archive read messages
        mv "$inbox" "$COMM_DIR/${agent_name}_read_$(date +%s).txt"
        echo "✅ Messages archived"
        return 0
    else
        return 1
    fi
}

broadcast_message() {
    local from_agent="$1"
    local message="$2"

    # Send to all known agents
    for session in $(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E '^(proj-|pm-)'); do
        if [ "$session" != "$from_agent" ]; then
            send_message "$from_agent" "$session" "$message"
        fi
    done
}

send_coordination_update() {
    local agent_name="$1"
    local status="$2"
    local details="$3"

    # Send status to orchestrator
    echo "[$timestamp] $agent_name STATUS: $status - $details" > "$COMM_DIR/orchestrator_updates.txt"

    # Send to Project Managers
    for pm_session in $(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep '^pm-'); do
        send_message "$agent_name" "$pm_session" "STATUS: $status - $details"
    done
}

# Main command interface
case "$1" in
    "send")
        send_message "$2" "$3" "$4"
        ;;
    "read")
        read_messages "$2"
        ;;
    "broadcast")
        broadcast_message "$2" "$3"
        ;;
    "status")
        send_coordination_update "$2" "$3" "$4"
        ;;
    *)
        echo "Usage: $0 {send|read|broadcast|status} [args...]"
        echo "  send <from> <to> <message>"
        echo "  read <agent_name>"
        echo "  broadcast <from> <message>"
        echo "  status <agent_name> <status> <details>"
        exit 1
        ;;
esac