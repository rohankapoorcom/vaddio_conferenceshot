"""Support for Vaddio Conferenceshot Cameras."""
import asyncio
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN, DATA_SCHEMA
from .device import VaddioDevice

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["switch", "camera"]


async def async_setup(hass: HomeAssistantType, config: dict):
    """Set up the Vaddio Conferenceshot Component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up an instance of a Vaddio Conferenceshot Camera from a config entry."""
    vaddio_device = VaddioDevice(**entry.data)
    await hass.async_add_executor_job(vaddio_device.retrieve_info)

    hass.data[DOMAIN][entry.entry_id] = vaddio_device

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


# SERVICE_RECALL_PRESET = "move_to_preset"
# ATTR_MAC_ADDRESS = "mac_address"
# ATTR_PRESET_ID = "preset"


# def _mac_address(value: str) -> str:
#     """Validate a Mac Address and convert to standard format."""
#     regex = re.compile("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$")
#     if not re.match(regex, value.lower()):
#         raise vol.Invalid("Invalid Mac Address")
#     return value.upper().replace("-", "").replace(":", "")
#
#
# RECALL_PRESET_SCHEMA = vol.Schema(
#     {
#         vol.Required(ATTR_MAC_ADDRESS): vol.All(cv.string, _mac_address),
#         vol.Required(ATTR_PRESET_ID): vol.All(
#             cv.positive_int, vol.Range(min=1, max=16)
#         ),
#     }
# )


# def setup(hass, config):
#     """Set up the Vaddio Conferenceshot Component."""
#
#     hass.data[DOMAIN] = {}
#
#     for conf in config[DOMAIN]:
#         vaddio_device = VaddioDevice(
#             conf[CONF_HOST], conf[CONF_USERNAME], conf[CONF_PASSWORD], conf[CONF_PATH]
#         )
#         vaddio_device.retrieve_info()
#         hass.data[DOMAIN][vaddio_device.mac_address] = vaddio_device
#
#     def recall_preset(call):
#         """Move the specified camera to the specified preset."""
#         vaddio_id = call.data[ATTR_MAC_ADDRESS]
#         if vaddio_id not in hass.data[DOMAIN]:
#             _LOGGER.error(
#                 "Invalid Vaddio Conferenceshot mac address provided: %s", vaddio_id
#             )
#             return
#
#         if not hass.data[DOMAIN][vaddio_id].is_on:
#             _LOGGER.error(
#                 "Unable to move Vaddio COnferenshot camera %s " "because it is off",
#                 vaddio_id,
#             )
#             return
#
#         preset_id = call.data[ATTR_PRESET_ID]
#         if not hass.data[DOMAIN][vaddio_id].move_to_preset(preset_id):
#             _LOGGER.error(
#                 "Unable to move Vaddio COnferenceshot camera %s to preset %s",
#                 vaddio_id,
#                 preset_id,
#             )
#             return
#
#     hass.services.register(
#         DOMAIN, SERVICE_RECALL_PRESET, recall_preset, schema=RECALL_PRESET_SCHEMA
#     )
#
#     for platform in ["switch", "camera"]:
#         hass.async_create_task(async_load_platform(hass, platform, DOMAIN, {}, config))
#     return True
