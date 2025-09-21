from __future__ import annotations

import voluptuous as vol
from urllib.parse import urlparse

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_URL,
    CONF_INTERVAL,
    DEFAULT_INTERVAL_MIN,
)

def _normalize_url(value: str) -> str:
    value = value.strip()
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.netloc:
        raise vol.Invalid("Invalid URL")
    return value

class PushToUptimeKumaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                url = _normalize_url(user_input[CONF_URL])
                interval = int(user_input[CONF_INTERVAL])
                if interval <= 0:
                    raise vol.Invalid("Interval must be positive")

                # unique_id = full URL
                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=urlparse(url).netloc,
                    data={
                        CONF_URL: url,
                        CONF_INTERVAL: interval,
                    },
                )
            except vol.Invalid:
                errors["base"] = "invalid_input"

        schema = vol.Schema(
            {
                vol.Required(CONF_URL): str,
                vol.Required(CONF_INTERVAL, default=DEFAULT_INTERVAL_MIN): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_import(self, user_input: dict | None = None) -> FlowResult:
        return await self.async_step_user(user_input)


class PushToUptimeKumaOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                interval = int(user_input[CONF_INTERVAL])
                if interval <= 0:
                    raise vol.Invalid("Interval must be positive")
                return self.async_create_entry(title="", data={CONF_INTERVAL: interval})
            except vol.Invalid:
                errors["base"] = "invalid_input"

        current_interval = self.config_entry.options.get(
            CONF_INTERVAL, self.config_entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL_MIN)
        )
        schema = vol.Schema({vol.Required(CONF_INTERVAL, default=current_interval): int})
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)


async def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> PushToUptimeKumaOptionsFlowHandler:
    return PushToUptimeKumaOptionsFlowHandler(config_entry)
