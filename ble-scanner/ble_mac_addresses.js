var getmac = require('getmac');
var noble = require('noble');
var mqtt = require('mqtt');


var client  = mqtt.connect('mqtt://192.168.1.2', {
  protocolId: 'MQIsdp',
  protocolVersion: 3
});

client.on('connect', function() { // When connected
   console.log("MQTT client connected!");  
});

client.on('offline', function() {
   console.log("MQTT client disconnected!");  
});

// Use our MAC address as a source identifier for this scanner
      getmac.getMac(function (err, mac_address) {
         if (err) {
            console.log('Could not get MAC address.');
            console.log(err);
         } else {
            console.log('Found mac address: ' + mac_address);

            noble.on('discover', function (peripheral) {
               manufac_data = '';

               console.log('peripheral discovered (' + peripheral.uuid.match(/../g).join(':') + '):');
               console.log('   hello my local name is: ' + peripheral.advertisement.localName);
               console.log('   ' + peripheral.rssi);

               if (peripheral.advertisement.manufacturerData) {
                  manufac_data = peripheral.advertisement.manufacturerData.toString('hex');
               }

               blob = {
                  location_str: 'unknown',
                  ble_addr: peripheral.uuid.match(/../g).join(':'),
                  name: peripheral.advertisement.localName,
                  scanner_macAddr: mac_address.toUpperCase(),
                  service_uuids: peripheral.advertisement.serviceUuids,
                  manufacturer_data: manufac_data,
                  rssi: peripheral.rssi,
                  time: Date.now()/1000,
               }

               // Publish advertisement to MQTT 
               client.publish('office/ble', JSON.stringify(blob), function() {
                  console.log("Message is published");
               });
            });
         }
      });

// Actually start receiving BLE advertisements
noble.on('stateChange', function (state) {
    console.log("Starting scan...");
    if (state === 'poweredOn') {
        noble.startScanning([], true);
    }
});
