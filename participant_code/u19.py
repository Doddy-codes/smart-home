from controller import Robot,DistanceSensor
from controller import Motor
from controller import PositionSensor
from termcolor import colored, cprint

#GLOBALS
Compass =  0
PositionX = 0
PositionY = 0
FrontLeft = 0
FrontRight = 0
RightFront = 0
RightBack = 0
BackLeft = 0
BackRight = 0
LeftBack = 0
LeftFront = 0
delay = 0

Front = 0 
ForntLeft = 0
Back = 0
BackLeft = 0
Back = 0
BackRight = 0
Right =  0
FrontRight = 0
#---------------------------------------------------------------------------------------------------------------# 
#INIT
robot = Robot() # Create robot object
timeStep = int(robot.getBasicTimeStep()) 
maxSpeed = 6.28

wheel_left = robot.getDevice("wheel1 motor")
wheel_left.setPosition(float('inf'))

wheel_right = robot.getDevice("wheel2 motor") 
wheel_right.setPosition(float('inf'))

distanceSensor1 = robot.getDevice("D1")
distanceSensor1.enable(timeStep) 

distanceSensor2 = robot.getDevice("D2")
distanceSensor2.enable(timeStep) 

distanceSensor3 = robot.getDevice("D3")
distanceSensor3.enable(timeStep) 

distanceSensor4 = robot.getDevice("D4")
distanceSensor4.enable(timeStep) 

distanceSensor5 = robot.getDevice("D5")
distanceSensor5.enable(timeStep) 

distanceSensor6 = robot.getDevice("D6")
distanceSensor6.enable(timeStep) 

distanceSensor7 = robot.getDevice("D7")
distanceSensor7.enable(timeStep) 

distanceSensor8 = robot.getDevice("D8")
distanceSensor8.enable(timeStep) 

iuSensor = robot.getDevice("inertial_unit") 
iuSensor.enable(timeStep)

gpsSensor = robot.getDevice("gps") 
gpsSensor.enable(timeStep)
#---------------------------------------------------------------------------------------------------------------#

#HELPER FUNCTIONS
def rad2deg(rad):
    return (rad/3.14)*180
def readSensorsU14():
    global Compass,Front,ForntLeft,Left,BackLeft,Back,BackRight,Right,FrontRight
    global US_Front,US_Left,US_Right
    Compass =  (rad2deg(iuSensor.getRollPitchYaw()[2]) + 360 )% 360

    Front = int(distanceSensor1.getValue() * 10 * 32)
    ForntLeft = int(distanceSensor2.getValue() * 10  * 32)
    Left = int(distanceSensor3.getValue() * 10 * 32)
    BackLeft = int(distanceSensor4.getValue()* 10 * 32)
    Back = int(distanceSensor5.getValue()* 10 * 32)
    BackRight = int(distanceSensor6.getValue()* 10 * 32)
    Right = int(distanceSensor7.getValue() * 10  * 32)
    FrontRight = int(distanceSensor8.getValue() * 10 * 32)
    US_Front = Front
    US_Left = FrontLeft
    US_Right = FrontRight
def debugU14():
    global Compass,Front,ForntLeft,Back,BackLeft,Back,BackRight,Right,FrontRight
    print()
    cprint("-------------------------------------","cyan",)
    cprint("----------------- Debug -------------","cyan",)
    cprint("-------------------------------------","cyan",)
    print()
    cprint("----------------- Distance -------------","yellow",)
    cprint("                       Front: " +str(Front),"yellow")
    cprint("        FrontLeft: " + str(FrontLeft) + "                 FrontRight: " + str(FrontRight),"yellow")
    cprint("Left: " + str(Left) + "                                             Right: " + str(Right),"yellow")
    cprint("        BackLeft: " + str(BackLeft) + "                   BackRight: " + str(BackRight),"yellow")
    cprint("                       Back: " + str(Back),"yellow")
    cprint("----------------- Compass -------------","yellow",)
    cprint("Compass: " + str("%.0f "%Compass),"yellow")


def readSensorsU19():
    global Compass,PositionX,PositionY,FrontLeft,FrontRight,RightFront,RightBack,BackLeft,BackRight,LeftBack,LeftFront
    Compass =  (rad2deg(iuSensor.getRollPitchYaw()[2]) + 360 )% 360
    PositionX = gpsSensor.getValues()[0] * 100
    PositionY = gpsSensor.getValues()[2] * 100
    FrontLeft = int(distanceSensor1.getValue() * 10 * 32)
    FrontRight = int(distanceSensor8.getValue() * 10 * 32)
    RightFront = int(distanceSensor7.getValue() * 10 * 32)
    RightBack = int(distanceSensor6.getValue()* 10 * 32)
    BackLeft = int(distanceSensor3.getValue()* 10 * 32)
    BackRight = int(distanceSensor5.getValue()* 10  * 32)
    LeftBack = int(distanceSensor4.getValue() *10 * 32)
    LeftFront = int(distanceSensor2.getValue()*10 * 32)

def debugU19():
    global Compass,PositionX,PositionY,FrontLeft,FrontRight,RightFront,RightBack,BackLeft,BackRight,LeftBack,LeftFront
    print()
    cprint("-------------------------------------","cyan",)
    cprint("----------------- Debug -------------","cyan",)
    cprint("-------------------------------------","cyan",)
    print()
    cprint("----------------- Distance -------------","yellow",)
    cprint("          Front: " +str(FrontLeft) + " " + str(FrontRight),"yellow")
    cprint("Left: " + str(LeftFront) + "                            Right: " + str(RightFront),"yellow")
    cprint("Left: " + str(LeftBack) + "                             Right: " + str(RightBack),"yellow")
    cprint("            Back: " + str(BackLeft) + " " + str(BackRight),"yellow")
    cprint("-----------------   GPS   -------------","cyan",)
    cprint("X: " + str("%.2f "%PositionX) + "           Y: "+str("%.2f "%PositionY),"blue")
    cprint("----------------- Compass -------------","yellow",)
    cprint("Compass: " + str("%.0f "%Compass),"yellow")
def move (left,right, d=0):
    global delay
    wheel_right.setVelocity(right * maxSpeed/10)
    wheel_left.setVelocity(left * maxSpeed/10)
    delay = d
#---------------------------------------------------------------------------------------------------------------#
#MAINWHILE (Start from here)

turnRightState = False
while robot.step(timeStep) != -1:
    readSensorsU19() #map sensors to human readable names
    debugU19() #print sensors information of console
  
    # move(0,0)
    if(delay > 0): # delay mechanism
        delay = delay - 1
    
    elif turnRightState: 
        move (10,-10,25)
        turnRightState = False
   
    elif (FrontLeft < 30 and FrontRight < 30):
        turnRightState = True
        move (-10,-10,15)     
   
    elif (FrontLeft < 30 ):
        move (-10,10)
   
    elif (FrontRight < 30 ):
        move (10,-10)
        
    else:
        move (10,10)
    