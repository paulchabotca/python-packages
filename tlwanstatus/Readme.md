# TL Wan Status

Retrieves status of wan device on a TP-Link TD-W9970. I imagine it would work on other TP-Link devices w/wo
some modifications..

## Usage

> use the sample dotenv or create one in your home directory

*.wanstat.env*
```
WANSTAT_ROUTERIP="192.168.0.1"
WANSTAT_USERNAME="Username"
WANSTAT_PASSWORD="Password"
WANSTAT_DEVICE="pppoe_ptm_35_3_d"
```
### Commands


*device-status*

Returns connection state as one of a few self explanatory strings ( *meant to be used as or with a service.* )
- Connected
- Initializing
- Disconnected

*list-wans*

Returns all wan connections from TD-W9970. Works with or without the dotenv. 

Options:
--action [all|type|vpid|ipmask|gateway|dns|status]
                                select information to return
--routerip TEXT                 The person to greet.
--username TEXT                 Username to WAN device
--password TEXT                 Password for wan device.
--device TEXT                   Optional Name of wan device, otherwise
                                returns all
--version
--help                          Show this message and exit.

[www.paulchabot.ca](https://www.paulchabot.ca)

## TODO

- add osx notification (requires db file, check last status, if changed, notify)
- add launchd script