# emulate multiple things sending data to thingspace.io at configured intervals
# thomas.amershek@verizon.com 2016/08/24

import random
import operator
# need to download this next library and install
# suggested download and run get-pip.py first for managing packages; use 'sudo python get-pip.py' once you download
# use 'sudo pip install requests'
import requests
import time
import json
# use fake-factory library for generating random GPS coordinates
# suggested download and run get-pip.py first for managing packages; use 'sudo python get-pip.py' once you download
# use 'sudo pip install fake-factory'
from faker import Factory
faker=Factory.create()

# define the names for your objects; define as many as you'd like
# *** PLEASE EDIT ***
nickname = raw_input("\nPlease enter device name:  ")
thingNames = [ nickname ]

# dictionary of attributes to provide a template for things
thingAttrs = {}

# a method for adding attributes with integer value ranges to your thing template
def addAttribute (name, lowValue, highValue):
	thingAttrs[name] = {}
	thingAttrs[name]['minValue'] = lowValue
	thingAttrs[name]['maxValue'] = highValue

# use the above method to add attributes to your object template
addAttribute(name = 'Temperature', lowValue = 64, highValue = 88)
addAttribute(name = 'Light', lowValue = 0, highValue = 1000)
addAttribute(name = 'Microphone', lowValue = 0, highValue = 100)
addAttribute(name = 'Potentiometer', lowValue = 0, highValue = 1000)

# move through the attribute dictionary and set random values for JSON payload
def getRandomJson () :
	jsonSend = {}
	for key, value in thingAttrs.items():
		jsonSend[key] = str(random.randint(value["minValue"], value["maxValue"]))
	# use fake-factory to add some random GPS coordinates while you're there ...
	jsonSend["GpsFix"] = "true"	
	jsonSend["Latitude"] = str(faker.latitude())
	jsonSend["Longitude"] = str(faker.longitude())
	return json.dumps(jsonSend, sort_keys=True)

def postData (thing):
	url = "https://thingspace.io/dweet/for/" + thing
	headers = {}
	headers['Content-Type'] = 'application/json'
	headers['Accept'] = 'application/json'
	response = requests.post(url, headers=headers, data=getRandomJson())
	
	# json.loads returns a dictionary version of the response.text JSON so that attributes can be referenced by name
	jsonResponse = json.loads(response.text)
	if response.status_code == requests.codes.ok:
		# json.dumps flattens the dictionary response for the change; opposite json.loads
		return jsonResponse["with"]["thing"] + ":  " + json.dumps(jsonResponse["with"]["content"], sort_keys=True)
	else:
		return json.dumps(jsonRespone)

print "\n***********************************\nVerizon ThingSpace Device Simulator\n***********************************\n"
while True:
	for thingName in thingNames:
		print postData(thing = thingName)
	waitTime = 5
	plural = ""
	if waitTime > 1:
		plural = "s"
	print "\nWait for " + str(waitTime) + " second" + plural + " ...\n"
	time.sleep(waitTime)
#end
