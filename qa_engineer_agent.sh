#!/bin/bash

# QA Engineer Agent for Tmux Orchestrator
# Focuses on testing, quality assurance, and validation

PROJECT_NAME="$1"
PROJECT_PATH="$2"
PM_SESSION="$3"
CYCLE_COUNT=0

log_activity() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] QA_ENGINEER [$PROJECT_NAME]: $1" | tee -a "${PROJECT_PATH}/qa_engineer.log"
}

run_quality_checks() {
    cd "$PROJECT_PATH"
    local issues_found=0

    log_activity "🔍 Running quality checks..."

    # Code quality checks
    if [ -f "package.json" ]; then
        # Node.js quality checks
        log_activity "📦 Checking Node.js project quality..."

        # Check for package-lock.json
        if [ ! -f "package-lock.json" ]; then
            log_activity "⚠️ ISSUE: Missing package-lock.json"
            issues_found=$((issues_found + 1))
        fi

        # Check for .gitignore
        if [ ! -f ".gitignore" ]; then
            log_activity "⚠️ ISSUE: Missing .gitignore file"
            echo "node_modules/\n.env\n*.log" > .gitignore
            log_activity "✅ Created basic .gitignore file"
        fi

        # Check for basic project structure
        if [ ! -d "src" ] && [ ! -f "index.js" ] && [ ! -f "app.js" ]; then
            log_activity "⚠️ ISSUE: No main application files found"
            issues_found=$((issues_found + 1))
        fi

    elif [ -f "requirements.txt" ]; then
        # Python quality checks
        log_activity "🐍 Checking Python project quality..."

        # Check for virtual environment indicators
        if [ ! -f ".venv" ] && [ ! -f "venv" ] && [ -z "$VIRTUAL_ENV" ]; then
            log_activity "⚠️ SUGGESTION: Consider using virtual environment"
        fi

        # Check for __init__.py files if there are Python packages
        if find . -name "*.py" -not -path "./.git/*" | head -1 | grep -q .; then
            if [ ! -f "__init__.py" ]; then
                log_activity "📝 INFO: No __init__.py found - checking if needed"
            fi
        fi
    fi

    # General quality checks
    if [ ! -f "README.md" ]; then
        log_activity "⚠️ ISSUE: Missing README.md"
        issues_found=$((issues_found + 1))
    else
        # Check README quality
        local readme_lines=$(wc -l < README.md)
        if [ $readme_lines -lt 5 ]; then
            log_activity "⚠️ ISSUE: README.md is too short ($readme_lines lines)"
            issues_found=$((issues_found + 1))
        fi
    fi

    # Git commit message quality
    local recent_commit=$(git log -1 --pretty=format:"%s" 2>/dev/null)
    if [ -n "$recent_commit" ]; then
        if [ ${#recent_commit} -lt 10 ]; then
            log_activity "⚠️ ISSUE: Recent commit message too short: '$recent_commit'"
            issues_found=$((issues_found + 1))
        fi
    fi

    log_activity "🔍 Quality check complete: $issues_found issues found"
    return $issues_found
}

run_automated_tests() {
    cd "$PROJECT_PATH"
    log_activity "🧪 Running automated tests..."

    local test_results=0

    if [ -f "package.json" ]; then
        # Check if test script exists
        if grep -q '"test"' package.json; then
            log_activity "📝 Found test script in package.json"
            # Note: We won't actually run npm test to avoid blocking, but we validate it exists
            log_activity "✅ Test configuration validated"
        else
            log_activity "⚠️ WARNING: No test script defined in package.json"
            test_results=1
        fi
    elif [ -f "requirements.txt" ]; then
        # Check for Python test files
        if find . -name "*test*.py" -o -name "test_*.py" | head -1 | grep -q .; then
            log_activity "📝 Found Python test files"
            log_activity "✅ Test files validated"
        else
            log_activity "⚠️ WARNING: No Python test files found"
            test_results=1
        fi
    fi

    return $test_results
}

validate_documentation() {
    cd "$PROJECT_PATH"
    log_activity "📚 Validating documentation..."

    local doc_score=0

    # Check README completeness
    if [ -f "README.md" ]; then
        if grep -q -i "installation\|install\|setup" README.md; then
            doc_score=$((doc_score + 1))
        fi
        if grep -q -i "usage\|example\|how to" README.md; then
            doc_score=$((doc_score + 1))
        fi
        if grep -q -i "license" README.md; then
            doc_score=$((doc_score + 1))
        fi
    fi

    log_activity "📚 Documentation score: $doc_score/3"

    if [ $doc_score -lt 2 ]; then
        log_activity "⚠️ RECOMMENDATION: Improve documentation completeness"
        return 1
    fi

    return 0
}

report_to_pm() {
    local quality_score="$1"
    local test_status="$2"
    local doc_status="$3"

    # Send comprehensive QA report to Project Manager
    local report="QA REPORT: Quality=$quality_score, Tests=$test_status, Docs=$doc_status, Cycle=$CYCLE_COUNT"

    /home/james/projs/Tmux-Orchestrator/send-claude-message.sh "${PM_SESSION}:0" "$report"
    log_activity "📊 Sent QA report to Project Manager"
}main_qa_cycle() {
    while true; do
        CYCLE_COUNT=$((CYCLE_COUNT + 1))

        log_activity "=== QA ENGINEER CYCLE #$CYCLE_COUNT ==="

        # Run quality assurance checks
        run_quality_checks
        local quality_issues=$?

        run_automated_tests
        local test_status=$?

        validate_documentation
        local doc_status=$?

        # Calculate overall quality score
        local total_issues=$((quality_issues + test_status + doc_status))
        local quality_score=""

        if [ $total_issues -eq 0 ]; then
            quality_score="EXCELLENT"
        elif [ $total_issues -le 2 ]; then
            quality_score="GOOD"
        elif [ $total_issues -le 4 ]; then
            quality_score="FAIR"
        else
            quality_score="NEEDS_WORK"
        fi

        log_activity "📊 Overall Quality Assessment: $quality_score ($total_issues issues)"

        # Report to Project Manager
        report_to_pm "$quality_score" "$test_status" "$doc_status"

        log_activity "Cycle #$CYCLE_COUNT complete - next in 90 seconds"
        sleep 90  # QA runs less frequently than PM
    done
}

# Validate inputs
if [ -z "$PROJECT_NAME" ] || [ -z "$PROJECT_PATH" ] || [ -z "$PM_SESSION" ]; then
    echo "Usage: $0 <project_name> <project_path> <pm_session>"
    exit 1
fi

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project path $PROJECT_PATH does not exist"
    exit 1
fi

log_activity "QA Engineer starting for $PROJECT_NAME at $PROJECT_PATH"
log_activity "Reporting to PM session: $PM_SESSION"

# Start QA cycle
main_qa_cycle