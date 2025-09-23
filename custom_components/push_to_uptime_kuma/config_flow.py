from __future__ import annotations

import voluptuous as vol
from urllib.parse import urlparse

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_URL,
    CONF_INTERVAL,
    DEFAULT_INTERVAL_SEC,
    MIN_INTERVAL_SEC,
    MAX_INTERVAL_SEC,
)


def _normalize_url(value: str) -> str:
    """Ensure the URL is valid and contains scheme + netloc."""
    value = value.strip()
    # If user forgot scheme, add https://
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.netloc:
        raise vol.Invalid("invalid_url")
    return value


class PushToUptimeKumaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                url = _normalize_url(user_input[CONF_URL])
            except vol.Invalid:
                errors["base"] = "invalid_url"
                url = None

            interval: int | None = None
            if not errors:
                try:
                    interval = int(user_input[CONF_INTERVAL])
                    if interval < MIN_INTERVAL_SEC or interval > MAX_INTERVAL_SEC:
                        raise vol.Invalid("invalid_interval")
                except (ValueError, vol.Invalid):
                    errors["base"] = "invalid_interval"

            if not errors and url and interval is not None:
                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=urlparse(url).netloc,
                    data={
                        CONF_URL: url,
                        CONF_INTERVAL: interval,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_URL): str,
                vol.Required(CONF_INTERVAL, default=DEFAULT_INTERVAL_SEC): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_import(self, user_input: dict | None = None) -> FlowResult:
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return PushToUptimeKumaOptionsFlowHandler(config_entry)


class PushToUptimeKumaOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                interval = int(user_input[CONF_INTERVAL])
                if interval < MIN_INTERVAL_SEC or interval > MAX_INTERVAL_SEC:
                    raise vol.Invalid("invalid_interval")
                return self.async_create_entry(title="", data={CONF_INTERVAL: interval})
            except (ValueError, vol.Invalid):
                errors["base"] = "invalid_interval"

        current_interval = self.config_entry.options.get(
            CONF_INTERVAL, self.config_entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL_SEC)
        )
        schema = vol.Schema({vol.Required(CONF_INTERVAL, default=current_interval): int})
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
