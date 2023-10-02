
from machine import Pin, SoftI2C, PWM, ADC
from files import *
import time
from machine import Timer
#import smarttools
import servo
import icons
import os
import sys
import ubinascii
import machine


import sensors
sens=sensors.SENSORS()

#unique name

ID= ubinascii.hexlify(machine.unique_id()).decode()
numberofIcons=[len(icons.iconFrames[i]) for i in range(len(icons.iconFrames))] #[homescreen, trainscreen, playscreen, playthefilesscreen, settingsscreen]
highlightedIcon=[]
for numberofIcon in numberofIcons:
    highlightedIcon.append([0,numberofIcon])

screenID=0
lastPressed=0
previousIcon=0
filenumber=0

points = []


#Defining all flags
#flags
flags=[False,False,False,False]

#switch flags
switch_state_up = False
switch_state_down = False
switch_state_select = False

last_switch_state_up = False
last_switch_state_down = False
last_switch_state_select = False

switched_up = False
switched_down = False
switched_select = False


#mainloop flags
clearscreen=False



#define buttons , sensors and motors
#servo
s = servo.Servo(Pin(2))

#nav switches
switch_down = Pin(8, Pin.IN)
switch_select = Pin(9, Pin.IN)
switch_up= Pin(10, Pin.IN)

i2c = SoftI2C(scl = Pin(7), sda = Pin(6))
display = icons.SSD1306_SMART(128, 64, i2c,switch_up)


#highlightedIcon=[(ICON,TotalIcons),...]
#screenID gives the SCREEN number I am at
#SCREENID
#0 - HOMESCREEN
#1 - PlaySCREEN
#2 - TrainSCREEN
#3 - Playthefiles
#4 - ConnectSCREEN

#highligtedIcons[screenID][0] which icon is highlighted on screenID screen
#highligtedIcons[screenID][0] =1 # First Icon selected
#highligtedIcons[screenID][0] =2 #Second
#highligtedIcons[screenID][0] =3 #Third

#interrupt functions
def downpressed(count=-1):
    time.sleep(0.1)
    if(time.ticks_ms()-lastPressed>500):
        displayselect(count)

    
def uppressed(count=1):
    time.sleep(0.1)
    if(time.ticks_ms()-lastPressed>500):
        displayselect(count)



def displayselect(selectedIcon):
    global screenID
    global highlightedIcon
    global lastPressed
    global previousIcon

    highlightedIcon[screenID][0]=(highlightedIcon[screenID][0]+selectedIcon)%highlightedIcon[screenID][1]
    display.selector(screenID,highlightedIcon[screenID][0],previousIcon) #draw circle at selection position, and remove from the previousIconious position
    previousIcon=highlightedIcon[screenID][0]

    lastPressed=time.ticks_ms()
    
def selectpressed():
    #declare all global variables, include all flags
    global flags
    time.sleep(0.1)
    flags[highlightedIcon[screenID][0]]=True


        
def resettohome():
    global screenID
    global highlightedIcon
    global previousIcon
    global clearscreen
    screenID=0
    previousIcon=0
    for numberofIcon in numberofIcons:
        highlightedIcon.append([0,numberofIcon])
    display.selector(screenID,highlightedIcon[screenID][0],0)
    #display.fill(0) # clear screen
    clearscreen=True
    
def check_switch(p):
    global switch_state_up
    global switch_state_down
    global switch_state_select
    
    global switched_up
    global switched_down
    global switched_select
    
    global last_switch_state_up
    global last_switch_state_down
    global last_switch_state_select
    
    switch_state_up = switch_up.value()
    switch_state_down = switch_down.value()
    switch_state_select = switch_select.value()
         
    if switch_state_up != last_switch_state_up:
        switched_up = True
        
    elif switch_state_down != last_switch_state_down:
        switched_down = True
        
    elif switch_state_select != last_switch_state_select:
        switched_select = True
        
        
    if switched_up:
        if switch_state_up == 0:
            uppressed()
        switched_up = False
    elif switched_down:
        if switch_state_down == 0:
            downpressed()
        switched_down = False
    elif switched_select:
        if switch_state_select == 0:
            selectpressed()
        switched_select = False
    
    last_switch_state_up = switch_state_up
    last_switch_state_down = switch_state_down
    last_switch_state_select = switch_state_select



def displaybatt(p):
    batterycharge=sens.readbattery()
    display.showbattery(batterycharge)
    return batterycharge



def nearestNeighbor(data, point):
    try:
        point = point[0]
    except TypeError:
        print("error")
        pass
    if len(data) == 0:
        return 0
    diff = 10000
    test = None
    for i in data:
        if abs(i[0] - point) <= diff:
            diff = abs(i[0] - point)
            test = i
    return test

def resetflags():
    global flags
    for i in range(len(flags)):
        flags[i]=False
    
    
    
#setting up Timers
tim = Timer(0)
tim.init(period=50, mode=Timer.PERIODIC, callback=check_switch)
batt = Timer(2)
batt.init(period=3000, mode=Timer.PERIODIC, callback=displaybatt)



display.welcomemessage()

#setup with homescreen  #starts with screenID=0
display.selector(screenID,highlightedIcon[screenID][0],-1)
oldpoint=[-1,-1]

def shakemotor(point):
    motorpos=point[1]
    for i in range(2):
        s.write_angle(motorpos+10)
        time.sleep(0.1)
        s.write_angle(motorpos-10)
        time.sleep(0.1)
        
    print(motorpos)
    
    
    
while True:
    point = sens.readpoint()
    #broadcast(point, screenID, highlightedIcon[screenID][0],ID)
    
    #Homepage
    #[fb_Train,fb_Play]


    if(screenID==0):
        if(flags[0]):
            points=[] #empty the points arrray
            screenID=1
            clearscreen=True
            display.graph(oldpoint, point, points)
            
        elif(flags[1]):
            screenID=3
            clearscreen=True
            datapoints=readfile()
            if (datapoints==[]):
                display.showmessage("No data saved")
                resettohome()
            else:
                display.graph(oldpoint, point, points)
            
        #elif(flags[2]):
        #    screenID=4
    
    # Training Screen
    # [fb_add,fb_delete,fb_smallplay,fb_home]
    elif(screenID==1):
        if(flags[0]):
            points.append(list(point))
            display.graph(oldpoint, point, points)
            shakemotor(point)
            
        elif(flags[1]):
            if(points): #delete only when there is something
                points.pop()
            display.cleargraph()
            display.graph(oldpoint, point, points)
                
        elif(flags[2]):
            if (points):
                screenID=2 # trigger play screen
                uppressed(count=4)
            else:
                display.showmessage("No data to run")
                resettohome()
 
        elif(flags[3]): #Home
           resettohome()
           
        if(not point==oldpoint): #only when point is different now
            s.write_angle(point[1])
            display.graph(oldpoint, point, points)

    #Play Screen
    #[fb_save,fb_pause,fb_home,fb_toggle]
    elif(screenID==2):
        if(flags[0]):  # save function here
            savetofile(points)
            uppressed(count=1)
           
        elif(flags[1]): # go home
            resettohome()
        
        #elif(flags[3]):  #toggle the data
        #    pass
            
        if(not point==oldpoint): #only when point is different now
            point = nearestNeighbor(points,point)
            print(point)
            s.write_angle(point[1])
            display.graph(oldpoint, point, points)

    
    # Load saved files screen
    #[fb_next,fb_delete,fb_home,fb_toggle]
    elif(screenID==3):
        datapoints=readfile()        
        if(datapoints):
            numberofdata=len(datapoints)
            points=datapoints[filenumber]
            
            if(flags[0]):
                filenumber=((filenumber+1)%numberofdata)
                points=datapoints[filenumber]
                display.cleargraph()
                
            elif(flags[1]):
                del datapoints[filenumber]
                replacefile(datapoints)
                filenumber=0
                display.cleargraph()

            elif(flags[2]):
                resettohome()
                
            if(not point==oldpoint): #only when point is different now
                point = nearestNeighbor(points,point)
                s.write_angle(point[1])
                display.graph(oldpoint, point, points)
        else:
            display.showmessage("No files to show")
            resettohome()
               
    # Settings Screen
    #[fb_Lead,fb_Follow, fb_BIGHome]
    elif(screenID==4):
        if(flags[0]):
            display.showmessage(ID)
            waitforconnection()
            
        elif(flags[1]):
            print("I shall follow you")
        
        elif(flags[2]):
            resettohome()
                    
    oldpoint=point
    resetflags()
    if clearscreen:
        display.fill(0)
        display.selector(screenID,highlightedIcon[screenID][0],-1)
        clearscreen=False









