# 1wire-connector
## Generates a json-file via the owfs with 1-wire sensor values.

Originaly designed to generate a json file with 1wire sensor values which can be read in by [edomi](http://www.edomi.de). In Edomi JSON can be read by the JSON Extractor LBS19001208, which can be found [here](https://service.knx-user-forum.de/?comm=download).

The 1wire data is grabbed by the [one wire file system](http://www.owfs.org).

Following owfs packages are used:
- owfs
- python-ow
- ow-shell

## Install
### OWFS:
`
apt-get install owfs python-ow ow-shell
`
and then configure to your needs.
  
### Copy files:
devices.json and read1w.py to `/var/www`
  
1wire-connector.service to `/etc/systemd/system/`
  
### Start service
`systemctl start 1wire-connector.service`
  
## What is working:
- [x] Get data from DS18B20 (temperature10 and power)
- [x] Get data from 2438 (smart battery monitor) (VDD, VAD, vis, humidity)
- [x] Add as systemd service
- [x] Device names can be defined via device.json


## Notes:
If you change the device.json, don't forgett to restart the service `systemctl restart 1wire-connector`
