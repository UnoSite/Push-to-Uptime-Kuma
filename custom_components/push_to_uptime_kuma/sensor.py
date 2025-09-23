from __future__ import annotations

from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import (
    DOMAIN,
    DATA_LAST_CALLED,
    DATA_INTERVAL,
    DATA_NETLOC,
    DATA_PING_MS,
)


def _format_interval(seconds: int) -> str:
    """Return a human readable string for the interval."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        sec = seconds % 60
        return f"{minutes}m {sec}s" if sec else f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        sec = seconds % 60
        parts = []
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if sec:
            parts.append(f"{sec}s")
        return " ".join(parts)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: DataUpdateCoordinator = data["coordinator"]
    netloc: str = data["netloc"]

    entities: list[SensorEntity] = [
        PushToUptimeKumaLastCalledSensor(coordinator, entry.entry_id, netloc),
        PushToUptimeKumaIntervalSensor(coordinator, entry.entry_id, netloc),
        PushToUptimeKumaPingSensor(coordinator, entry.entry_id, netloc),
    ]
    async_add_entities(entities)


class _BaseKumaSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: DataUpdateCoordinator, entry_id: str, netloc: str):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._netloc = netloc

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name=self._netloc,
            manufacturer="Uptime Kuma",
            model="Push Monitor",
        )


class PushToUptimeKumaLastCalledSensor(_BaseKumaSensor):
    _attr_name = "Last called"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: DataUpdateCoordinator, entry_id: str, netloc: str):
        super().__init__(coordinator, entry_id, netloc)
        self._attr_unique_id = f"{entry_id}_last_called"

    @property
    def native_value(self) -> datetime | None:
        return self.coordinator.data.get(DATA_LAST_CALLED)


class PushToUptimeKumaIntervalSensor(_BaseKumaSensor):
    _attr_name = "Call interval"
    _attr_native_unit_of_measurement = "s"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: DataUpdateCoordinator, entry_id: str, netloc: str):
        super().__init__(coordinator, entry_id, netloc)
        self._attr_unique_id = f"{entry_id}_call_interval"

    @property
    def native_value(self) -> int | None:
        return int(self.coordinator.data.get(DATA_INTERVAL, 0))

    @property
    def extra_state_attributes(self):
        seconds = self.native_value or 0
        return {
            "human_readable": _format_interval(seconds)
        }


class PushToUptimeKumaPingSensor(_BaseKumaSensor):
    _attr_name = "Ping time"
    _attr_native_unit_of_measurement = "ms"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: DataUpdateCoordinator, entry_id: str, netloc: str):
        super().__init__(coordinator, entry_id, netloc)
        self._attr_unique_id = f"{entry_id}_ping_ms"

    @property
    def native_value(self) -> int | None:
        return self.coordinator.data.get(DATA_PING_MS)
