from __future__ import annotations

DOMAIN = "push_to_uptime_kuma"

CONF_URL = "url"
CONF_INTERVAL = "interval"  # minutes

DEFAULT_INTERVAL_MIN = 5

PLATFORMS = ["sensor"]

# Data keys stored in coordinator.data
DATA_LAST_CALLED = "last_called"
DATA_INTERVAL = "interval"
DATA_URL = "url"
DATA_NETLOC = "netloc"

LOGGER_NAME = f"custom_components.{DOMAIN}"
