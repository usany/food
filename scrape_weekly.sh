#!/usr/bin/env bash
# Weekly menu scrape — runs the 5 Playwright jobs sequentially, then exits.
#
# Replaces the old always-on APScheduler (restaurants/scheduler.py and
# restaurants/management/commands/run_scheduler.py). No resident process:
# this only exists for the ~5 minutes of actual work each Friday night.
#
# Used three ways:
#   1. systemd timer  -> deploy/food-scrape.service
#   2. host cron      -> deploy/crontab
#   3. Docker         -> docker compose run --rm --no-deps scraper
#
# Safe to run manually to re-scrape after a failure:
#   sudo -u ubuntu /home/ubuntu/food/scrape_weekly.sh

set -uo pipefail

export TZ="${TZ:-Asia/Seoul}"

# Overridable for Docker (APP_DIR=/app PYTHON=python); defaults target the
# host venv at /home/ubuntu/food/.venv.
APP_DIR="${APP_DIR:-/home/ubuntu/food}"
PYTHON="${PYTHON:-$APP_DIR/.venv/bin/python}"

cd "$APP_DIR" || { echo "ERROR: cannot cd to $APP_DIR" >&2; exit 1; }
command -v "$PYTHON" >/dev/null 2>&1 || { echo "ERROR: python not found: $PYTHON" >&2; exit 1; }

log() { echo "[$(date '+%F %T %Z')] $*"; }

failures=0

run_job() {
    log "START playwright $*"
    if "$PYTHON" manage.py playwright "$@"; then
        log "OK    playwright $*"
    else
        log "FAIL  playwright $* (exit $?)"
        failures=$((failures + 1))
    fi
}

log "========== weekly scrape beginning =========="

run_job --source khu  --campus seoul
run_job --source khu  --campus global
run_job --source hufs --student
run_job --source hufs
run_job --source dorm

log "========== weekly scrape finished: $failures failed =========="
exit "$failures"
