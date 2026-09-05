# Deployment (no persistent scheduler)

Replaces the old always-on APScheduler container with short-lived, once-a-week
jobs. The web app (gunicorn) is the only always-running process — the scheduler
process that used to sit idle 24/7 is gone.

## What's here

| File | Purpose |
|---|---|
| `../scrape_weekly.sh` | runs all 5 Playwright jobs sequentially, then exits |
| `food-web.service` | gunicorn web server (always on) |
| `food-scrape.service` + `food-scrape.timer` | systemd timer, Fridays 23:05 KST |
| `crontab` | cron alternative to the systemd timer |

## One-time server setup

```bash
# 1. system packages
sudo apt-get update && sudo apt-get install -y python3-venv python3-pip

# 2. venv + dependencies (requires requirements.txt — see Notes)
cd /home/ubuntu/food
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
sudo .venv/bin/playwright install-deps chromium   # apt deps for headless chromium

# 3. prepare the script + logs dir
chmod +x scrape_weekly.sh
mkdir -p logs
```

## systemd (recommended)

```bash
sudo cp deploy/food-web.service deploy/food-scrape.service deploy/food-scrape.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now food-web food-scrape.timer
sudo systemctl status food-web food-scrape.timer
```

- Logs: `journalctl -u food-web -f` and `journalctl -u food-scrape -f`
- Test a scrape now: `sudo systemctl start food-scrape`
- Next scheduled run: `systemctl list-timers food-scrape.timer`

## cron alternative

```bash
crontab deploy/crontab
```

## Docker (if you keep the web in Docker)

`docker-compose.yml` now has a one-off `scraper` service (no `restart`). Trigger
it from host cron:

```cron
05 23 * * 5  cd /home/ubuntu/food && docker compose run --rm --no-deps scraper
```

## Notes

- `.env` must use plain `KEY=value` lines (no `export`), otherwise systemd's
  `EnvironmentFile` will reject it.
- `restaurants/scheduler.py`, `restaurants/management/commands/run_scheduler.py`,
  and the `apscheduler` dependency are now unused — delete them.
- `requirements.txt` doesn't exist yet; extract it from the Dockerfile's
  `pip install` list so local venv and Docker share one dependency source.
