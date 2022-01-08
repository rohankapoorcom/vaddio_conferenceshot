from homeassistant.components.camera import Camera, SUPPORT_STREAM
from homeassistant.helpers.device_registry import format_mac

from .const import DOMAIN
from .device import VaddioDevice

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup the Vaddio Conferenceshot switch platform from a config entry."""
    vaddio_device = hass.data[DOMAIN][config_entry.entry_id]

    if vaddio_device.streaming_enabled:
        async_add_entities([VaddioCamera(vaddio_device)], False)


class VaddioCamera(Camera):
    """Representation of a Vaddio Camera."""

    def __init__(self, vaddio_device):
        """Initialize as a subclass of GenericCamera."""
        super().__init__()
        self._vaddio_device = vaddio_device
        self._name = vaddio_device.name
        self._stream_source = "rtsp://{}:{}/{}".format(
            vaddio_device._hostname, vaddio_device._streaming_port, vaddio_device._path
        )
        self._unique_id = format_mac(vaddio_device._mac_address)

    @property
    def supported_features(self):
        """Return supported features for this camera."""
        return SUPPORT_STREAM

    @property
    def name(self):
        """Return the name of this device."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique_id of this device."""
        return self._unique_id

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, format_mac(self._vaddio_device._mac_address))},
            "name": self._vaddio_device.name,
            "manufacturer": VaddioDevice.manufacturer,
            "model": self._vaddio_device.model,
            "sw_version": self._vaddio_device.version,
            "configuration_url": f"http://{self._vaddio_device._hostname}",
        }

    async def stream_source(self):
        """Return the source of the stream."""
        return self._stream_source
