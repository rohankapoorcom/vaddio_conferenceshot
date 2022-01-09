import logging

from homeassistant import config_entries, exceptions
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN, DATA_SCHEMA
from .device import VaddioDevice

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistantType, data: dict) -> VaddioDevice:
    """Validate the user input allows us to connect.
    Data has the keys from DATA_SCHEMA with the values provided by the user.
    """
    vaddio_device = VaddioDevice(**data)

    response = await hass.async_add_executor_job(vaddio_device.test_connection)

    if not response:
        raise CannotConnect

    response = await hass.async_add_executor_job(vaddio_device.test_auth)

    if not response:
        raise InvalidAuth

    await hass.async_add_executor_job(vaddio_device.retrieve_info)
    return vaddio_device


class VaddioConferenceShotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vaddio Conferenceshot."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            vaddio_device = None
            try:
                vaddio_device = await validate_input(self.hass, user_input)

            except CannotConnect:
                errors["base"] = "cannot_connect"

            except InvalidAuth:
                errors["base"] = "invalid_auth"

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if vaddio_device is not None:
                await self.async_set_unique_id(format_mac(vaddio_device._mac_address))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Vaddio {vaddio_device.model}", data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
