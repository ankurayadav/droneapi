import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
	print ser.readline()
	if (int(ser.readline())<200 and int(ser.readline())>0):
		print "hi"
