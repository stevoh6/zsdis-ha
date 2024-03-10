"""Sensor platform for ZSDIS HA."""
import json
from datetime import datetime, timezone, timedelta
from homeassistant.components.mqtt import CONF_STATE_TOPIC, subscribe
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

def setup_platform(hass: HomeAssistant, config: ConfigType, add_entities, discovery_info=None):
    """Set up the sensor platform from configuration.yaml."""
    # This assumes your MQTT topic is configured in the platform configuration in configuration.yaml
    topic = config.get(CONF_STATE_TOPIC)
    name = config.get(CONF_NAME, "ZSDIS Electricity Usage")

    @callback
    def message_received(msg):
        """Handle new MQTT messages."""
        payload = json.loads(msg.payload)
        state_value = payload.get("state")
        datetime_str = payload.get("datetime")

        # Convert the timestamp to a datetime object
        message_datetime = datetime.fromtimestamp(datetime_str, tz=timezone.utc)

        # Get yesterday's date
        yesterday = datetime.now(tz=timezone.utc) - timedelta(days=1)
        if message_datetime.date() == yesterday.date():
            # If the message is from yesterday, update the sensor
            sensor = ZSDISElectricityUsageSensor(name, state_value)
            add_entities([sensor])

    subscribe(hass, topic, message_received)

class ZSDISElectricityUsageSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name: str, state):
        """Initialize the sensor."""
        self._state = state
        self._name = name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._name}_electricity_usage"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "kWh"