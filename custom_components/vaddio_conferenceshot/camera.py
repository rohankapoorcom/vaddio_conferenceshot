from homeassistant.components.generic.camera import (
    CONF_STILL_IMAGE_URL,
    CONF_STREAM_SOURCE,
    GenericCamera,
    PLATFORM_SCHEMA,
)
from homeassistant.const import CONF_NAME, CONF_PLATFORM


from . import DOMAIN as VADDIO_DOMAIN


async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the Vaddio Conferenceshot switch platform."""
    switches = []
    for _, vaddio_device in hass.data[VADDIO_DOMAIN].items():
        switches.append(VaddioCamera(hass, vaddio_device))
    add_entities(switches)
    return True


class VaddioCamera(GenericCamera):
    """Representation of a Vaddio Camera."""

    def __init__(self, hass, vaddio_device):
        """Initialize as a subclass of GenericCamera."""
        camera_url = "rtsp://{}:554{}".format(
            vaddio_device._hostname, vaddio_device._path
        )

        device_info = PLATFORM_SCHEMA(
            {
                CONF_PLATFORM: VADDIO_DOMAIN,
                CONF_NAME: vaddio_device.name,
                CONF_STILL_IMAGE_URL: camera_url,
                CONF_STREAM_SOURCE: camera_url,
            }
        )
        super().__init__(hass, device_info)
