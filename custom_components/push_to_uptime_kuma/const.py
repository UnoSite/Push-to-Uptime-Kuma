from __future__ import annotations

DOMAIN = "push_to_uptime_kuma"

CONF_URL = "url"
CONF_INTERVAL = "interval"  # seconds

DEFAULT_INTERVAL_SEC = 60
MIN_INTERVAL_SEC = 20
MAX_INTERVAL_SEC = 86400  # 24 hours

PLATFORMS = ["sensor"]

# Data keys stored in coordinator.data
DATA_LAST_CALLED = "last_called"
DATA_INTERVAL = "interval"
DATA_URL = "url"
DATA_NETLOC = "netloc"

LOGGER_NAME = f"custom_components.{DOMAIN}"
