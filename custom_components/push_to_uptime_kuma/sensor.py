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
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: DataUpdateCoordinator = data["coordinator"]
    netloc: str = data["netloc"]

    entities: list[SensorEntity] = [
        PushToUptimeKumaLastCalledSensor(coordinator, entry.entry_id, netloc),
        PushToUptimeKumaIntervalSensor(coordinator, entry.entry_id, netloc),
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
