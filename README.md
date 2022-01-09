# Vaddio Conferenceshot integration for Home Assistant

The Vaddio Conferenceshot integration allows for the control of a Vaddio Conferenceshot, Conferenceshot AV, Clearshot or Roboshot camera from Home Assistant.

These cameras expose a telnet interface for getting their status as well as controlling them.

Currently Supports:
- Switch entity for turning on/off the camera.
- Camera entity for viewing the RTSP streaming feed from cameras that support it.
- The `camera` entity has a service that allows you to send the camera to a saved preset. See `custom_components/vaddio_conferenceshot/services.yaml` for documentation on the service call.

# Installation

The easiest way to install is through HACS. The Vaddio Conferenceshot integration is **not** included in the HACS default repositories so it will have to be added manually.

1. In Home Assistant, select HACS -> Integrations -> Custom repositories. Add `https://github.com/rohankapoorcom/vaddio_conferenceshot` in the `Integration` category.
2. In Home Assistant, select HACS -> Integrations -> + Explore and Download Repositories. Search for Vaddio Conferenceshot in the list and add it.
3. Restart Home Assistant
4. Set up and configure the integration: [![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=vaddio_conferenceshot)

You will need your camera's IP address / Hostname and admin credentials to set up the integration.

## Manual Installation

Copy the `custom_components/vaddio_conferenceshot` directory to your `custom_components` folder. Restart Home Assistant, and add the integration from the integrations page.

# Contributing
Contributions are welcome! Please open a Pull Request with your changes.