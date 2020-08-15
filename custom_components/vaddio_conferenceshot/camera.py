from homeassistant.components.camera import (
    CONF_STILL_IMAGE_URL,
    CONF_STREAM_SOURCE,
    Camera,
    PLATFORM_SCHEMA,
    SUPPORT_STREAM
)
from homeassistant.const import CONF_NAME, CONF_PLATFORM


from . import DOMAIN as VADDIO_DOMAIN


async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the Vaddio Conferenceshot switch platform."""
    cameras = []
    for _, vaddio_device in hass.data[VADDIO_DOMAIN].items():
        cameras.append(VaddioCamera(vaddio_device))
    add_entities(cameras)
    return True


class VaddioCamera(Camera):
    """Representation of a Vaddio Camera."""

    def __init__(self, vaddio_device):
        """Initialize as a subclass of GenericCamera."""
        super().__init__()
        self._name = vaddio_device.name
        self._stream_source = "rtsp://{}:554{}".format(
            vaddio_device._hostname, vaddio_device._path
        )

    @property
    def supported_features(self):
        """Return supported features for this camera."""
        return SUPPORT_STREAM

    def camera_image(self):
        """Return bytes of camera image."""
        return None

    @property
    def name(self):
        """Return the name of this device."""
        return self._name

    async def stream_source(self):
        """Return the source of the stream."""
        if self._stream_source is None:
            return None

        try:
            return self._stream_source.async_render()
        except TemplateError as err:
            _LOGGER.error("Error parsing template %s: %s", self._stream_source, err)
            return None
