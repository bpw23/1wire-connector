#!/usr/bin/python2 -u

import io
import json
import timeit
import time

import ow


if __name__ == "__main__":
    while True:
        # read device list
        with open('devices.json') as json_file:
            devicelist = json.load(json_file)
        # outputlist as dict
        outputlist = {}

        # connect to owfs
        ow.init('localhost:4304')

	# Enable simultaneous temperature conversation
	ow._put("simultaneous/temperature","1")
	#ow._put("simultaneous/voltage","1")

        # read in connected sensor
        sensorlist = ow.Sensor('/').sensorList()
	#print(sensorlist)

        # loop through sensors and read values
        for sensor in sensorlist:
	    try:
                sensorvalues={}
                #print('Family: ' + sensor.family)
                #print('ID: ' + sensor.id)
                #print('Type: ' + sensor.type)
                sensorvalues["name"] = devicelist[sensor.id]

		if sensor.family == "28":
                    sensorvalues["temperature10"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/temperature10")
                    sensorvalues["power"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/power")
                elif sensor.family == "26":
                    sensorvalues["VAD"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/VAD")
                    sensorvalues["VDD"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/VDD")
                    sensorvalues["vis"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/vis")
                    sensorvalues["humidity"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/humidity")

            except KeyError:
	        sensorvalues["name"] = ""
		print("Error: The sensor [" + sensor.family + "." + sensor.id + "]  generates -sensorvalues KeyError-")
		continue

	    except ow.exUnknownSensor, e:
    	        sensorvalues["Error"]="Sensor lost"
		print("Sensor lost")
		continue

	    outputlist[sensor.family+"."+sensor.id] = sensorvalues
	    #print('----------------------------')
	# Put general infos into file
	outputlist["info"] = {"error":"","Number_of_devices":len(sensorlist),"1wire_connector_version":"1","Last_refresh":time.strftime("%d.%m.%Y %H:%M:%S")}
	
	# Put info into file on error
	if outputlist =="":
	    outpulist={"info":{"error":"No devices found"}}

	# write to output json file
	try:
	    with io.open('1wire.json', 'w', encoding='utf8') as f:
	        f.write(unicode(json.dumps(outputlist, ensure_ascii=False, indent=4)))
	    print ('1wire.json written - ' + time.strftime("%d.%m.%Y  %H:%M:%S"))
	except IOError:
	    print("Can't write 1wire.json !")
