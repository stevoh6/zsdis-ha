"""The ZSDIS HA integration."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, PLATFORMS

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the ZSDIS HA component from configuration.yaml."""
    # Forward the setup to your platform(s)
    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
    return True
