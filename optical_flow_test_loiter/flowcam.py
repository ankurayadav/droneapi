#!/usr/bin/env python
from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time
from cv import *

def mavrx_debug_handler(message):
    """A demo of receiving raw mavlink messages"""
    print "Received", message

# First get an instance of the API endpoint
api = local_connect()
# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]

def mode_callback(attribute):
    print "Mode changed: ", v.mode

def hover():
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

    time.sleep(8)

    print "Hover Throttle"
    v.channel_override = { "3" : 1500}
    v.flush()
    
    time.sleep(1)

class FBackDemo:
    def __init__(self):
        #self.capture = CaptureFromCAM(0)
	self.capture = CaptureFromFile("http://@192.168.0.97:8080/?action=stream/frame.mjpg")
        #SetCaptureProperty(self.capture, 3, 160)
        #SetCaptureProperty(self.capture, 4, 120)
        #SetCaptureProperty(self.capture, CV_CAP_PROP_POS_FRAMES, 10)
        #does not work, this was a try to reduce the delay.
        self.mv_step = 8
        self.mv_scale = 1.5
        self.mv_color = (0, 255, 0)
        self.mv_color2 = (255,0,0)
        self.cflow = None
        self.flow = None
        self.font1 = InitFont(CV_FONT_HERSHEY_COMPLEX, 1, 1, 0, 1, 8)
        self.original_frame = None

        NamedWindow( "Optical Flow", 1 )

        print( "Press q - quit the program\n" )

    def draw_flow(self, flow, prevgray,tm):
        """ Returns a nice representation of a hue histogram """
        k = .5
        CvtColor(prevgray, self.cflow, CV_GRAY2BGR)
        left=0
        right=0
        for y in range(0, flow.height, self.mv_step):
            for x in range(0, flow.width/2, self.mv_step):
                fx, fy = flow[y, x]
                if (abs(fx) > k) and (abs(fy) > k):
                    color = self.mv_color
                    left = left+1
                else:
                    color = self.mv_color2
                Line(self.cflow, (x,y), (int(x+fx),int(y+fy)), color)
                Circle(self.cflow, (x,y), 1, color, -1)        
        
        for y in range(0, flow.height, self.mv_step):
            for x in range(flow.width/2, flow.width, self.mv_step):
                fx, fy = flow[y, x]
                if (abs(fx) > k) and (abs(fy) > k):
                    color = self.mv_color2
                    right=right+1
                else:
                    color = self.mv_color
                Line(self.cflow, (x,y), (int(x+fx),int(y+fy)), color)
                Circle(self.cflow, (x,y), 1, color, -1)
      
        Resize(self.cflow,self.original_frame)
        
	if(right<20)and(left<20):
	    print "No Hurddle"
	    #print "Roll neutral"
            v.channel_override = { "1" : 1500}
            v.flush()
            #time.sleep(1)
        else:
	    if(left>right):
	        print "left"
            	#print "Roll channel"
            	v.channel_override = { "1" : 1400}
            	v.flush()
            	#time.sleep(2)
	    else:
            	print "right"
            	#print "Roll channel"
            	v.channel_override = { "1" : 1600}
            	v.flush()
            	#time.sleep(2)
       
	#PutText (self.original_frame,"tm "+str(tm)+"s", (10,50), self.font1, (0,0,255));
        ShowImage("Optical Flow", self.original_frame)

    def run(self):
        first_frame = True
        frame = CreateImage((320,240), 8, 3)
        while True:
            self.original_frame = QueryFrame( self.capture )
            while self.original_frame is None:
                print "Lost frame... trying again"
                self.original_frame = QueryFrame (self.capture) 

            Resize(self.original_frame,frame)
            Flip(frame,None,1)
            if first_frame:
                gray = CreateImage(GetSize(frame), 8, 1)
                prev_gray = CreateImage(GetSize(frame), 8, 1)
                flow = CreateImage(GetSize(frame), 32, 2)
                self.cflow = CreateImage(GetSize(frame), 8, 3)
                first_frame = False

            CvtColor(frame, gray, CV_BGR2GRAY)
            if not first_frame:
                t = time.time()                        
                CalcOpticalFlowFarneback(prev_gray, gray, flow,
                    pyr_scale=0.5, levels=3, winsize=15,
                    iterations=2, poly_n=5, poly_sigma=1.1, flags=0)
                self.draw_flow(flow, prev_gray,time.time()-t)
                c = WaitKey(7)
                if c == ord("q"):
                    break
            prev_gray,gray = gray, prev_gray
            

hover()    
demo = FBackDemo()
demo.run()
