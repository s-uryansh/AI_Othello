#!/usr/bin/env bash
set -euo pipefail
# ... Create collection dir ...
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COLLECT_DIR="$ROOT_DIR/logs/collected"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "$COLLECT_DIR"

# -----------------------
# 1) Run backend unit tests
# -----------------------
echo "Running backend pytest..."
(
  cd "$ROOT_DIR/backend"
  # Ensure PYTHONPATH includes backend so tests can import app
  PYTHONPATH=. pytest -q 2>&1 | tee "$COLLECT_DIR/backend_pytest_$TIMESTAMP.log"
)

# -----------------------
# 2) Run demo scripts (short demos)
# -----------------------
echo "Running demo_all_agents (short) ..."
(
  cd "$ROOT_DIR/backend"
  PYTHONPATH=. python -u app/scripts/demo_all_agents.py 2>&1 | tee "$COLLECT_DIR/demo_all_agents_$TIMESTAMP.log"
)

# -----------------------
# 3) Analyze validation results (generate plots) if data exists
# -----------------------
echo "Generating validation plots (if validation summary exists)..."
(
  cd "$ROOT_DIR/backend"
  PYTHONPATH=. python -u app/scripts/analyze_validation_results.py 2>&1 | tee "$COLLECT_DIR/analyze_validation_$TIMESTAMP.log" || true
)

# -----------------------
# 4) Collect backend app/logs into collected folder
# -----------------------
echo "Collecting backend logs..."
mkdir -p "$COLLECT_DIR/backend_app_logs_$TIMESTAMP"
if [ -d "$ROOT_DIR/backend/app/logs" ]; then
  cp -r "$ROOT_DIR/backend/app/logs/." "$COLLECT_DIR/backend_app_logs_$TIMESTAMP/" || true
fi

# -----------------------
# 5) Optional: frontend build (commented out by default)
# -----------------------
# echo "Running frontend build (optional)..."
# (
#   cd "$ROOT_DIR/frontend"
#   npm ci
#   npm run build 2>&1 | tee "$COLLECT_DIR/frontend_build_$TIMESTAMP.log"
# )

# -----------------------
# Done — summary
# -----------------------
echo "All tasks completed. Collected logs are in: $COLLECT_DIR"
ls -la "$COLLECT_DIR" | sed -n '1,200p'
