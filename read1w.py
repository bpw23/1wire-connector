#!/usr/bin/python2 -u

import ow
import io
import json


if __name__ == "__main__":
    # read device list
    with open('devices.json') as json_file:
        devicelist = json.load(json_file)

    # outputlist as dict
    outputlist = {}

    # connect to owfs
    ow.init('localhost:4304')

    # read in connected sensor
    sensorlist = ow.Sensor('/').sensorList()

    # loop through sensors and read values
    for sensor in sensorlist:
        sensorvalues={}
        #print('Family: ' + sensor.family)
        #print('ID: ' + sensor.id)
        #print('Type: ' + sensor.type)
        try:
	    #print('Name: ' + devicelist[sensor.id])
	    sensorvalues["name"] = devicelist[sensor.id]
	except KeyError:
	    #print('Name: -')
	    sensorvalues["name"] = " "
        if sensor.family == "28":
            sensorvalues["temperature10"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/temperature10")
	    sensorvalues["power"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/power")
        elif sensor.family == "26":
	    sensorvalues["VAD"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/VAD")
	    sensorvalues["VDD"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/VDD")
	    sensorvalues["vis"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/vis")
	    sensorvalues["humidity"]=ow.owfs_get("/bus.0/"+sensor.family+"."+sensor.id+"/humidity")
        outputlist[sensor.family+"."+sensor.id]=sensorvalues
        #print('----------------------------')

    # write to output json file
    with io.open('1wire.json', 'w', encoding='utf8') as f:
        f.write(unicode(json.dumps(outputlist, ensure_ascii=False, indent=4)))

    #print ('1wire.json written')


