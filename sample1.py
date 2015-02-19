from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

def mavrx_debug_handler(message):
    """A demo of receiving raw mavlink messages"""
    print "Received", message

# First get an instance of the API endpoint
api = local_connect()
# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]

def mode_callback(attribute):
    print "Mode changed: ", v.mode

#print "Disarming..."
#v.armed = False
#v.flush()

print "Initializing by default values"
v.channel_override = { "1" : 1500, "2" : 1499, "3" : 1102, "4" : 1510, "5" : 1099, "6" : 1901, "7" : 1099, "8" : 1500}
v.flush()

time.sleep(2)

v.channel_override = { "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0}
v.flush()

time.sleep(2)

v.mode = VehicleMode("LOITER")

time.sleep(2)

print "Arming..."
v.armed = True
v.flush()

time.sleep(2)

print "Increasing Throttle"
v.channel_override = { "3" : 1150 }
v.flush()

time.sleep(1)

print "Increasing Throttle"
v.channel_override = { "3" : 1200 }
v.flush()

time.sleep(1)

print "Increasing Throttle"
v.channel_override = { "3" : 1300 }
v.flush()

time.sleep(1)

print "Increasing Throttle"
v.channel_override = { "3" : 1400 }
v.flush()

time.sleep(1)

print "Increasing Throttle"
v.channel_override = { "3" : 1450 }
v.flush()

time.sleep(1)

print "Increasing Throttle 1500"
v.channel_override = { "3" : 1500 }
v.flush()

time.sleep(1)

print "Increasing Throttle 1550"
v.channel_override = { "3" : 1550 }
v.flush()

time.sleep(1)

print "Increasing Throttle 1600"
v.channel_override = { "3" : 1600 }
v.flush()

time.sleep(1)

print "Increasing Throttle 1630"
v.channel_override = { "3" : 1630 }
v.flush()

time.sleep(12)

print "Hover Throttle"
v.channel_override = { "3" : 1500}
v.flush()

time.sleep(1)

print "Yaw channel"
v.channel_override = { "4" : 1600}
v.flush()

time.sleep(5)

print "Yaw neutral"
v.channel_override = { "4" : 1510}
v.flush()

time.sleep(5)

print "Roll channel"
v.channel_override = { "1" : 1600}
v.flush()

time.sleep(5)

print "Roll neutral"
v.channel_override = { "1" : 1500}
v.flush()

time.sleep(5)

print "Pitch channel"
v.channel_override = { "2" : 1600}
v.flush()

time.sleep(5)

print "Pitch neutral"
v.channel_override = { "2" : 1499}
v.flush()

time.sleep(5)

v.mode = VehicleMode("LAND")

print "Cancelling Throttle Override"
v.channel_override = { "3" : 0 }
v.flush()
