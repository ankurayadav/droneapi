from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time
import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

def mavrx_debug_handler(message):
    """A demo of receiving raw mavlink messages"""
    print "Received", message

# First get an instance of the API endpoint
api = local_connect()
# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]

def mode_callback(attribute):
    print "Mode changed: ", v.mode

while True:
	if (int(ser.readline())<200 and int(ser.readline())>0):
		v.mode = VehicleMode("LAND")
		v.channel_override = { "3" : 0 }
		v.flush()
