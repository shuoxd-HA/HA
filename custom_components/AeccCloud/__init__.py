import logging

from homeassistant.components import zeroconf
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, SupportsResponse
from homeassistant.const import Platform


from .const import DOMAIN, BASE_URL  

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up the sensor platform from a config entry."""
    # Initialize your integration here (e.g., fetch data)
    hass.data.setdefault(DOMAIN, {})
    print("初始化成功")
    return True
