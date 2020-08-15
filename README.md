The Vaddio Conferenceshot integration allows for the control of a Vaddio Conferenceshot, Conferenceshot AV, or Clearshot camera with Home Assistant.

These cameras expose a telnet interface for getting their status as well as controlling them. This integration adds support for a very limited set of commands at this point. More can be added if there is a desire/request for them.

Pull requests are welcome.

Basic configuration example. Replace the host with the ip address or hostname of your camera and add it's admin credentials. Unfortunately, these cameras only expose their telnet interface to the admin user. After restarting Home Assistant, a new switch and camera component will be available.

```
vaddio_conferenceshot:
   - host: 192.168.1.100
     username: admin
     password: passsword
```

This integration exposes a service to move the camera to a desired preset position. The MAC Address can be formatted with dashes, colons or without separators. They will be all be converted to the same representation internally. The preset is an integer number between 1 and 16 (inclusive).

The service call looks like this:

```
vaddio_conferenceshot.move_to_preset:
  mac_address: "AB:78:37:E4:D5:E0"
  preset: 3
```
