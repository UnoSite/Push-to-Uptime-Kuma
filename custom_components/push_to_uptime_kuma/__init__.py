from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Callable
from urllib.parse import urlparse

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_URL,
    CONF_INTERVAL,
    DEFAULT_INTERVAL_MIN,
    PLATFORMS,
    DATA_LAST_CALLED,
    DATA_INTERVAL,
    DATA_URL,
    DATA_NETLOC,
    LOGGER_NAME,
)

import logging

_LOGGER = logging.getLogger(LOGGER_NAME)

type HassJobCancel = Callable[[], None]


class KumaPushRunner:
    """Handles periodic HTTP push."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: DataUpdateCoordinator,
    ) -> None:
        self.hass = hass
        self.entry = entry
        self.coordinator = coordinator
        self._cancel: HassJobCancel | None = None

    @property
    def interval_minutes(self) -> int:
        return _get_entry_interval(self.entry)

    def start(self) -> None:
        interval = timedelta(minutes=self.interval_minutes)
        self._cancel = async_track_time_interval(
            self.hass, self._handle_tick, interval
        )
        self.hass.async_create_task(self._do_push_and_update())

    def stop(self) -> None:
        if self._cancel:
            self._cancel()
            self._cancel = None

    async def _handle_tick(self, _now) -> None:
        await self._do_push_and_update()

    async def _do_push_and_update(self) -> None:
        url: str = self.entry.data[CONF_URL]
        session = aiohttp_client.async_get_clientsession(self.hass)
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if 200 <= resp.status < 300:
                    last_called = datetime.now().astimezone()
                    data = dict(self.coordinator.data or {})
                    data[DATA_LAST_CALLED] = last_called
                    data[DATA_INTERVAL] = self.interval_minutes
                    self.coordinator.async_set_updated_data(data)
                    _LOGGER.debug("Pushed to Uptime Kuma OK (%s)", resp.status)
                else:
                    _LOGGER.warning("Uptime Kuma push returned status %s", resp.status)
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout pushing to Uptime Kuma")
        except aiohttp.ClientError as err:
            _LOGGER.warning("HTTP error pushing to Uptime Kuma: %s", err)


def _get_entry_interval(entry: ConfigEntry) -> int:
    return int(entry.options.get(CONF_INTERVAL, entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL_MIN)))


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    parsed = urlparse(entry.data[CONF_URL])
    netloc = parsed.netloc

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DOMAIN}_{netloc}",
        update_method=None,
    )
    coordinator.data = {
        DATA_LAST_CALLED: None,
        DATA_INTERVAL: _get_entry_interval(entry),
        DATA_URL: entry.data[CONF_URL],
        DATA_NETLOC: netloc,
    }

    runner = KumaPushRunner(hass, entry, coordinator)
    runner.start()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "runner": runner,
        "netloc": netloc,
    }

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    return True


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    stored = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if not stored:
        return
    runner: KumaPushRunner = stored["runner"]
    coordinator: DataUpdateCoordinator = stored["coordinator"]

    runner.stop()
    data = dict(coordinator.data or {})
    data[DATA_INTERVAL] = _get_entry_interval(entry)
    coordinator.async_set_updated_data(data)
    runner.start()
    _LOGGER.debug("Options updated; runner restarted for %s", entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])
    stored = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if stored:
        runner: KumaPushRunner = stored["runner"]
        runner.stop()
    if not hass.data.get(DOMAIN):
        hass.data.pop(DOMAIN, None)
    return unload_ok
