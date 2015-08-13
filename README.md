##Node-RED Adapters##

Programs that produce data and send it into an MQTT queue (or websockets or what have you), which can be accessed by Node-RED (and other things).

### Adapters ###

**lan-scanner**
   - **lan_mac_addresses.py:** Uses nmap to get the wifi/ethernet MAC addresses of all devices on the LAN and sends the list to MQTT.

### To Do ###
   - BLE MAC address scanner.
   - Python object/package that can be imported and inherited in order to hide the whole MQTT thing. Will make writing these very fast.
