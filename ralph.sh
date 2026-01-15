#!/bin/bash

# =============================================================================
# Ralph Wiggum Loop - Autonomous Development Script
# =============================================================================
# Usage: ./ralph.sh [max_iterations]
# Example: ./ralph.sh 50
# =============================================================================

set -e

# Configuration
MAX_ITERATIONS=${1:-50}
ITERATION=0
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="${PROJECT_DIR}/logs"
COMPLETION_PHRASE="COMPLETE"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Helper Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Count remaining tasks (tasks with "passes": false)
count_remaining() {
    grep -c '"passes": false' "${PROJECT_DIR}/plan.json" 2>/dev/null || echo "0"
}

# Count completed tasks
count_completed() {
    grep -c '"passes": true' "${PROJECT_DIR}/plan.json" 2>/dev/null || echo "0"
}

# Check if all tasks are complete
all_done() {
    local remaining=$(count_remaining)
    [ "$remaining" -eq 0 ]
}

# =============================================================================
# Pre-flight Checks
# =============================================================================

echo ""
echo "=========================================="
echo "  Ralph Wiggum Loop - Starting"
echo "=========================================="
echo ""

cd "$PROJECT_DIR"

# Ensure required directories exist
mkdir -p "$LOG_DIR" screenshots

# Check for required files
if [ ! -f "plan.json" ]; then
    log_error "plan.json not found. Please create it first."
    exit 1
fi

if [ ! -f "PROMPT.md" ]; then
    log_error "PROMPT.md not found. Please create it first."
    exit 1
fi

if [ ! -f "activity.md" ]; then
    log_error "activity.md not found. Please create it first."
    exit 1
fi

# Check for claude CLI
if ! command -v claude &> /dev/null; then
    log_error "claude CLI not found. Please install it first."
    exit 1
fi

# Display initial status
TOTAL_TASKS=$(($(count_remaining) + $(count_completed)))
log_info "Project directory: $PROJECT_DIR"
log_info "Max iterations: $MAX_ITERATIONS"
log_info "Total tasks: $TOTAL_TASKS"
log_info "Completed: $(count_completed)"
log_info "Remaining: $(count_remaining)"
echo ""

# =============================================================================
# Main Loop
# =============================================================================

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    REMAINING=$(count_remaining)
    COMPLETED=$(count_completed)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    LOG_FILE="${LOG_DIR}/iteration_${ITERATION}.log"

    echo ""
    echo "=========================================="
    echo "  Iteration $ITERATION / $MAX_ITERATIONS"
    echo "  Time: $TIMESTAMP"
    echo "  Progress: $COMPLETED / $TOTAL_TASKS tasks"
    echo "  Remaining: $REMAINING"
    echo "=========================================="
    echo ""

    # Check if all tasks are complete
    if all_done; then
        echo ""
        echo "=========================================="
        log_success "ALL TASKS COMPLETE!"
        echo "  Total iterations: $ITERATION"
        echo "  Time: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "=========================================="
        echo ""
        exit 0
    fi

    # Run Claude with the prompt
    log_info "Starting Claude agent..."

    # Invoke Claude Code
    # --print: Output to stdout
    # --dangerously-skip-permissions: Skip permission prompts for autonomous execution
    claude --print --dangerously-skip-permissions \
        "Read PROMPT.md and follow the instructions exactly.
         Then read activity.md for context on what was done previously.
         Then read plan.json to find the next task with passes: false.
         Implement that ONE task, verify it, update activity.md and plan.json, commit, and output <promise>COMPLETE</promise>." \
        2>&1 | tee "$LOG_FILE"

    # Check for completion signal
    if grep -q "<promise>${COMPLETION_PHRASE}</promise>" "$LOG_FILE" 2>/dev/null; then
        log_success "Task completed, starting next iteration..."
        sleep 2
    else
        log_warning "No completion signal received"
        log_info "Check $LOG_FILE for details"
        log_info "Waiting 5 seconds before retry..."
        sleep 5
    fi

done

# =============================================================================
# Max Iterations Reached
# =============================================================================

echo ""
echo "=========================================="
log_warning "Max iterations reached: $MAX_ITERATIONS"
echo "  Completed: $(count_completed) / $TOTAL_TASKS"
echo "  Remaining: $(count_remaining)"
echo "=========================================="
echo ""

exit 1
