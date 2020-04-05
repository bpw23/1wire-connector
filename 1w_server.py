#!/usr/bin/python3 -u

from pyownet import protocol
import io
import os
import json
import timeit
import time
import logging


if __name__ == "__main__":
    sudoPassword = ''
    path_to_devices = ''
    path_to_log = ''

    restart_counter = 0

    logger = logging.getLogger('1w_server')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(path_to_log + '1w_server.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info('## Starting 1Wire-Server ####################################################################')

    while True:

        # read device list
        with open(path_to_devices + 'devices.json') as json_file:
            devicelist = json.load(json_file)
        # outputlist as dict
        outputlist = {}

        # connect to owfs
        owproxy = protocol.proxy(host='192.168.0.17', port=4304)

	    # Enable simultaneous temperature conversation
        owproxy.write("/simultaneous/temperature",b'1')
	    #ow._put("simultaneous/voltage","1")

        # read in connected sensor
        try:
            sensorlist = owproxy.dir(path='/', slash=False, timeout=0)

            # loop through sensors and read values
            for sensor in sensorlist:
                try:
                    sensorvalues = {}
                    # print('Sensor: ' + sensor)
                    # print('ID: ' + sensor.id)
                    # print('Type: ' + sensor.type)
                    sensorvalues["name"] = devicelist[sensor[1:]]
                    if sensor[1:3] == "28":
                        sensorvalues["temperature10"] = float(owproxy.read(sensor + "/temperature10"))
                        sensorvalues["power"] = float(owproxy.read(sensor + "/power"))
                    elif sensor[1:3] == "26":
                        sensorvalues["VAD"] = float(owproxy.read(sensor + "/VAD"))
                        sensorvalues["VDD"] = float(owproxy.read(sensor + "/VDD"))
                        sensorvalues["vis"] = float(owproxy.read(sensor + "/vis"))
                        sensorvalues["humidity"] = float(owproxy.read(sensor + "/humidity"))
                        sensorvalues["pressure"] = float(owproxy.read(sensor + "/B1-R1-A/pressure"))
                        sensorvalues["temperature"] = float(owproxy.read(sensor + "/temperature"))

                except KeyError:
                    logger.error(
                        f"Error: The sensor [{sensor}]  generates -sensorvalues KeyError- Set a name in devices.json!")
                    sensorvalues["name"] = ""
                    continue

                except Exception as  e:
                    sensorvalues["Error"] = f"Sensor lost: {e}"
                    logger.error(f"Sensor lost: {e}")
                    continue

                outputlist[sensor[1:]] = sensorvalues

        except protocol.OwnetError as e:
            #sudo killall owfs
            if sudoPassword != '':
                command = 'killall owfs'
                p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
                restart_counter += 1
                logger.error(f'OwnetError: This exception is raised to signal an error return code by the owserver [{e}]. Tried to kill owfs server with relpy: {p}')
            else:
                logger.error(f'OwnetError: This exception is raised to signal an error return code by the owserver [{e}]. Can not kill owfs, no sudo pwd is set!')
        except Exception as e:
            logger.error(f'getting sensorlist runs into error: {e}')

        # set errors
        info_error=""
        if len(sensorlist) == 0:
            info_error="No 1wire-devices found!"

        # Put general infos into file
        outputlist["info"] = {"error":info_error,"Number_of_devices":len(sensorlist),
			      "1wire_connector_version":"2",
			      "Last_refresh":time.strftime("%d.%m.%Y %H:%M:%S"),
			      "CRC8_errors":int(owproxy.read("/statistics/errors/CRC8_errors")),
			      "CRC16_errors":int(owproxy.read("/statistics/errors/CRC16_errors")),
			      "BUS_detect_errors":int(owproxy.read("/statistics/errors/BUS_detect_errors")),
                  "tried_owfs_restarts":restart_counter}

	    # write to output json file
        try:
            with io.open('1wire.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(outputlist, ensure_ascii=False, indent=4))
                logger.debug('1wire.json successfully written')
        except IOError:
            logger.error("Can't write 1wire.json !")

