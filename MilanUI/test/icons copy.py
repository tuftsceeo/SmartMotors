import framebuf
import ssd1306
from machine import Pin
import time



MAX_BATTERY=2900
MIN_BATTERY=2600


#define icons here
def createIcons(iconSize, iconFrames, offsetx=0, offsety=0, direction=0):
    icons=[]
    padding=2
    spacingV=int((screenHeight - iconSize*len(iconFrames))/ (len(iconFrames))-padding)
    spacingH=int((screenWidth - iconSize*len(iconFrames))/ (len(iconFrames))-padding)
    
    for i in range(len(iconFrames)):
        Iconx=offsetx + i * (spacingH + iconSize) * ((direction+1)%2)
        Icony=offsety# + i * (spacingV + iconSize) * ((direction)%2)

        icons.append([Iconx,Icony,iconFrames[i]])
        print(icons)
    return icons




#Homescreen icons
Icons=[]

screenWidth=128
screenHeight=120

#logo
fb_SMLOGO = framebuf.FrameBuffer(bytearray(b'\x00\x00\x01\xe0\x00\x00\x00\x00\x00\xe1\xe1\xc0\x00\x00\x00\x00\xff\xff\xc0\x00\x00\x00\x00\xff\xff\xc0\x00\x00\x00\x11\xff\xff\xe2\x00\x00\x00\x7f\xff\xff\xff\x80\x00\x00\x7f\xff\xff\xff\x80\x00\x00?\xff\xff\xff\x00\x00\x00\x7f\xff\xff\xff\x80\x00\x06\xff\xf0\x03\xff\xd8\x00\x07\xff\xc0\x00\xff\xf8\x00\x0f\xff\x00\x00?\xfc\x00\x07\xfe\x00\x00\x1f\xf8\x00\x07\xfc\x00\x00\x0f\xf8\x00\x07\xf8\x00\x00\x07\xf8\x00\x0f\xf0\x00\x00\x03\xfc\x00\x7f\xe0\x00\x00\x01\xff\x80\x7f\xe0\x00\x00\x01\xff\x80\x7f\xc0\x00\x00\x00\xff\x80?\xc0\x00\x00\x00\xff\x00\x1f\xc0\x00\x00\x00\xfe\x00\x1f\x80\x00\x00\x00~\x00?\x80\x00\x00\x00\x7f\x00\xff\x80\x00\x079\xbf\xc0\xff\x80\x00\x07\xbd\xbf\xc0\xff\x80\x00\x079\xbf\xc0\xff\x80\x00\x00\x00\xff\xc0?\x80\x00\x00\x00\x7f\x00\x1f\xc0\x00\x00\x00\xfe\x00\x1f\xc0\x00\x00\x00\xfe\x00?\xc0\x00\x00\x00\xff\x00\x7f\xe0\x00\x00\x01\xff\x80\x7f\xe0\x00\x00\x01\xff\x80\x7f\xf0\x00\x00\x03\xff\x80\x0f\xf0\x00\x00\x03\xfc\x00\x07\xf8\x00\x00\x07\xf8\x00\x03\xfc\x00\x00\x0f\xf0\x00\x07\xff\x00\x00?\xf8\x00\x0f\xff\x80\x00\x7f\xfc\x00\x07\xff\xe0\x01\xff\xf8\x00\x06\x7f\xfe\x1f\xff\x98\x00\x00?\xff\xff\xff\x00\x00\x00?\xff\xff\xff\x00\x00\x00\x7f\xff\xff\xff\x80\x00\x00{\xff\xff\xf7\x80\x00\x00\x10\xff\xff\xc2\x00\x00\x00\x00\xff\xff\xc0\x00\x00\x00\x00\xf1\xe3\xc0\x00\x00\x00\x00\xe1\xe1\xc0\x00\x00\x00\x00\x01\xe0\x00\x00\x00'), 50, 50, framebuf.MONO_HLSB)
#plug
fb_battcharging = framebuf.FrameBuffer(bytearray(b'?\xff\xff\xc0 \x00\x00@ \x06\x00@\xe0\x07\x80@\xe0\x7f\xc0@\xe0<\x00@\xe0\x0c\x00@ \x00\x00@ \x00\x00@?\xff\xff\xc0'), 26, 10, framebuf.MONO_HLSB)
fb_batthigh = framebuf.FrameBuffer(bytearray(b'?\xff\xff\xc0 \x00\x00@/\xef\xef@\xef\xef\xef@\xef\xef\xef@\xef\xef\xef@\xef\xef\xef@/\xef\xef@ \x00\x00@?\xff\xff\xc0'), 26, 10, framebuf.MONO_HLSB)
fb_battmid = framebuf.FrameBuffer(bytearray(b'?\xff\xff\xc0 \x00\x00@ \x0f\xef@\xe0\x0f\xef@\xe0\x0f\xef@\xe0\x0f\xef@\xe0\x0f\xef@ \x0f\xef@ \x00\x00@?\xff\xff\xc0'), 26, 10, framebuf.MONO_HLSB)
fb_battlow = framebuf.FrameBuffer(bytearray(b'?\xff\xff\xc0 \x00\x00@ \x00\x0f@\xe0\x00\x0f@\xe0\x00\x0f@\xe0\x00\x0f@\xe0\x00\x0f@ \x00\x0f@ \x00\x00@?\xff\xff\xc0'), 26, 10, framebuf.MONO_HLSB)


#HomeScreen Icons
fb_Train = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\xff\xff\x01\x80\x80\x01\x01\x80\x80\x01\x01\x80\xe0\x01\x01\x81\xf0\x01\x01\x81\xf8\x01\x01\x83\xf8\x01\x01\x81\xf0\x01\x01\x81\xf0A\x01\x80\xe0\x81\x01\x81\xf1\x81\x01\x83\xfb\x01\x01\x83\xfe\x01\x01\x87\xfc\x01\x01\x87\xfc\x01\x01\x87\xff\xff\x01\x87\xfc\x00\x01\x87\xfc\x00\x01\x87\xfc\x00\x01\x83\xf8\x00\x01\x83\xf8\x00\x01\x81\xf0\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\xff\xff\xff\xff'), 32, 32, framebuf.MONO_HLSB)
fb_Setting = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x01\xc3\x01\x81\xc3\xc7\x81\x81\xe3\xc7\x81\x81\xff\xef\x01\x81\xff\xff\x01\x80\xff\xfe\x19\x80\xfc?9\xb9\xf0\x0f\xfd\xbf\xe0\x07\xfd\xbf\xc0\x03\xfd\xbf\x80\x01\xf1\x93\x80\x01\xc1\x83\x80\x01\xc1\x83\x80\x01\xd9\xbf\x80\x01\xfd\xbf\xc0\x03\xfd\xbf\xe0\x07\xfd\xbf\xf0\x0f\x85\x9c\xfc?\x01\x80\x7f\xff\x81\x80\x7f\xff\xc1\x80\xff\xef\x81\x81\xf1\xe3\x81\x81\xe3\xe1\x81\x80\xe3\xe0\x01\x80\x00\x00\x01\x80\x00\x00\x01\xff\xff\xff\xff'), 32, 32, framebuf.MONO_HLSB)
fb_Play = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\x80\x00\x00\x01\x81\x00\x00\x01\x81\xc0\x00\x01\x81\xe0\x00\x01\x81\xf8\x00\x01\x81\xfe\x00\x01\x81\xff\x00\x01\x81\xff\xc0\x01\x81\xff\xe0\x01\x81\xff\xf8\x01\x81\xff\xfe\x01\x81\xff\xff\x01\x81\xff\xff\xc1\x81\xff\xff\xe1\x81\xff\xff\xf9\x81\xff\xff\xe1\x81\xff\xff\xc1\x81\xff\xff\x01\x81\xff\xfe\x01\x81\xff\xf8\x01\x81\xff\xe0\x01\x81\xff\xc0\x01\x81\xff\x00\x01\x81\xfe\x00\x01\x81\xf8\x00\x01\x81\xe0\x00\x01\x81\xc0\x00\x01\x81\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\xff\xff\xff\xff'), 32, 32, framebuf.MONO_HLSB)

#TrainScreen Icons
fb_add = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x1e\x00\x80\x80\x1e\x00\x80\x80\x1e\x00\x80\x80\x1e\x00\x80\x83\xff\xe0\x80\x83\xff\xe0\x80\x83\xff\xe0\x80\x83\xff\xe0\x80\x80\x1e\x00\x80\x80\x1e\x00\x80\x80\x1e\x00\x80\x80\x1e\x00\x80\x80\x1e\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_delete = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x8c\x00\x18\x80\x9e\x00<\x80\x8f\x00x\x80\x87\x80\xf0\x80\x83\xc1\xe0\x80\x81\xe3\xc0\x80\x80\xf7\x80\x80\x80\x7f\x00\x80\x80>\x00\x80\x80>\x00\x80\x80\x7f\x00\x80\x80\xff\x80\x80\x81\xe3\xc0\x80\x83\xc1\xe0\x80\x87\x80\xf0\x80\x8f\x00x\x80\x9f\x00|\x80\x8c\x00\x18\x80\x8c\x00\x18\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_smallplay = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x83\x00\x00\x80\x83\xc0\x00\x80\x83\xf0\x00\x80\x83\xf8\x00\x80\x83\xfe\x00\x80\x83\xff\x80\x80\x83\xff\xc0\x80\x83\xff\xf0\x80\x83\xff\xf0\x80\x83\xff\xc0\x80\x83\xff\x80\x80\x83\xfe\x00\x80\x83\xf8\x00\x80\x83\xf0\x00\x80\x83\xc0\x00\x80\x83\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_back = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x07\x80\x80\x80\x0f\x80\x80\x80\x1f\x80\x80\x80>\x00\x80\x80~\x00\x80\x80\xf8\x00\x80\x81\xf8\x00\x80\x83\xe0\x00\x80\x83\xe0\x00\x80\x81\xf8\x00\x80\x80\xf8\x00\x80\x80~\x00\x80\x80>\x00\x80\x80\x1f\x80\x80\x80\x0f\x80\x80\x80\x07\x80\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)

fb_upnobox = framebuf.FrameBuffer(bytearray(b'\x04\x00\x0e\x00\x1f\x00?\x80\x7f\xc0\xff\xe0\x1f\x00\x1f\x00'), 11, 8, framebuf.MONO_HLSB)
fb_downnobox = framebuf.FrameBuffer(bytearray(b'\x1f\x00\x1f\x00\xff\xe0\x7f\xc0?\x80\x1f\x00\x0e\x00\x04\x00'), 11, 8, framebuf.MONO_HLSB)
#PlayScreen Icons

fb_home = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80>\x00\x80\x80\x7f\x00\x80\x80\xff\x80\x80\x81\xff\xc0\x80\x83\xff\xe0\x80\x87\xff\xf0\x80\x8f\xff\xf8\x80\x9f\xff\xfc\x80\xbf\xff\xfe\x80\x87\xff\xf0\x80\x87\xff\xf0\x80\x87\xc1\xf0\x80\x87\xc1\xf0\x80\x87\xc1\xf0\x80\x87\xc1\xf0\x80\x87\xc1\xf0\x80\x87\xc1\xf0\x80\x87\xc1\xf0\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_pause = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\xc1\x80\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x81\xe3\xc0\x80\x80\xc1\x80\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_save = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x9f\xfe\x00\x80\x9f\xff\x00\x80\x9c\x03\x80\x80\x9c\x03\xc0\x80\x9c\x03\xe0\x80\x9c\x03\xf0\x80\x9c\x03\xf8\x80\x9f\xff\xf8\x80\x9f\xff\xfc\x80\x9f\xff\xfc\x80\x9f\xfc<\x80\x9f\xf8\x1c\x80\x9f\xf8\x1c\x80\x9f\xf8\x1c\x80\x9f\xf8\x1c\x80\x9f\xfc<\x80\x9f\xff\xfc\x80\x9f\xff\xfc\x80\x9f\xff\xfc\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_toggle = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x87\xf8\x00\x80\x84\x08\x00\x80\x84\x08\x00\x80\x84\x08\x00\x80\x84\x08\x00\x80\x84\x08\x00\x80\x9c\x0f\xfc\x80\x9c\x0f\xfc\x80\x9c\x0f\xfc\x80\x84\x08\x00\x80\x84\x08\x00\x80\x84\x08\x00\x80\x84\x08\x00\x80\x84\x08\x00\x80\x87\xf8\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)


#load saved files
fb_prev = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x07\x80\x80\x80\x0f\x80\x80\x80\x1f\x80\x80\x80>\x00\x80\x80~\x00\x80\x80\xf8\x00\x80\x81\xff\xf0\x80\x83\xff\xf0\x80\x83\xff\xf0\x80\x81\xff\xf0\x80\x80\xf8\x00\x80\x80~\x00\x80\x80>\x00\x80\x80\x1f\x80\x80\x80\x0f\x80\x80\x80\x07\x80\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_next = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\xf0\x00\x80\x80\xf8\x00\x80\x80\xfc\x00\x80\x80>\x00\x80\x80?\x00\x80\x80\x0f\x80\x80\x87\xff\xc0\x80\x87\xff\xe0\x80\x87\xff\xe0\x80\x87\xff\xc0\x80\x80\x0f\x80\x80\x80?\x00\x80\x80>\x00\x80\x80\xfc\x00\x80\x80\xf8\x00\x80\x80\xf0\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)
fb_load = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\x80\x80\x00\x00\x80\x80\x7f\x00\x80\x80\x7f\x00\x80\x80\x7f\x00\x80\x80\x7f\x00\x80\x80\x7f\x00\x80\x80\x7f\x00\x80\x80\x7f\x00\x80\x80\x7f\x00\x80\x83\xff\xe0\x80\x81\xff\xc0\x80\xb0\xff\x86\x80\xb0\xff\x86\x80\xb0\x7f\x06\x80\xb0>\x06\x80\xb0>\x06\x80\xb0\x1c\x06\x80\xb0\x18\x06\x80\xb0\x08\x06\x80\xbf\xff\xfe\x80\xbf\xff\xfe\x80\x80\x00\x00\x80\x80\x00\x00\x80\xff\xff\xff\x80'), 25, 25, framebuf.MONO_HLSB)

#Settings
fb_BIGHome = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x01\x80\x01\x80\x03\xc0\x01\x80\x0f\xf0\x01\x80\x1f\xf8\x01\x80?\xfc\x01\x80\x7f\xfe\x01\x81\xff\xff\x81\x83\xff\xff\xc1\x87\xff\xff\xe1\x8f\xff\xff\xf1\x83\xff\xff\xc1\x83\xff\xff\xc1\x83\xff\xff\xc1\x83\xd7\x1f\xc1\x83\xff\x1f\xc1\x83\xd7\x1f\xc1\x83\xff\x1f\xc1\x83\xff\x1f\xc1\x83\xff\x1f\xc1\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\xff\xff\xff\xff'), 32, 32, framebuf.MONO_HLSB)
fb_Lead = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x83\xf8\x0f\xe1\x82\x00\x00!\x82\x00\x00!\x82x\x0f!\x82@\x01!\x82@\x01!\x82L\x19!\x82H\t!\x82I\xc9!\x82I\xc9!\x82I\xc9!\x82H\x89!\x82@\x81!\x82@\x81!\x82p\x87!\x82\x00\x80!\x82\x00\x80!\x83\xf8\x8f\xe1\x80\x00\x80\x01\x80\x00\x80\x01\x80\x00\x80\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\xff\xff\xff\xff'), 32, 32, framebuf.MONO_HLSB)
fb_Follow = framebuf.FrameBuffer(bytearray(b'\xff\xff\xff\xff\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x07\xe0\x01\x80\x0c0\x01\x80\x10\x08\x01\x80 \x04\x01\x80@\x02\x01\x80@\x02\x01\x80@\x02\x01\x80@\x02\x01\x80@\x02\x01\x80 \x04\x01\x80\x10\x0c\x01\x80\x0c<\x01\x80\x07\xee\x01\x80\x00\x07\x01\x80\x00\x03\x81\x80\x00\x01\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\x80\x00\x00\x01\xff\xff\xff\xff'), 32, 32, framebuf.MONO_HLSB)

#Add the icons to the array, add iconsizes add the direction 0 - horizontal , 1 - vertical
#iconFrames=[[fb_Train,fb_Play,fb_Setting],[fb_add,fb_delete,fb_smallplay,fb_home],[fb_save,fb_pause,fb_home,fb_toggle],[fb_next,fb_delete,fb_home,fb_toggle],[fb_Lead,fb_Follow, fb_BIGHome]]
iconFrames=[[fb_Train,fb_Play],[fb_add,fb_delete,fb_smallplay,fb_home],[fb_save,fb_home],[fb_next,fb_delete,fb_home]]
iconSize=[32,25,25,25]
offsets= [(5,20),(102,29),(102,29),(102,29)] #where you want to display your first icon
direction=[0,1,1,1]                # 0 horizonal and 1 vertical arrangement

for index,icon in enumerate(iconFrames):
    icons = createIcons(iconSize[index], icon, offsetx=offsets[index][0], offsety=offsets[index][1] , direction=direction[index])
    Icons.append(icons)

class SSD1306_SMART(ssd1306.SSD1306_I2C):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False, scale = 8, mode = 0, plotsize = [[3,3],[100,60]]):
        self.scale = scale
        self.mode = mode # 0 for learn, 1 for repeat
        self.plotsize = plotsize
        self.ranges = {'light': [0, 4095], 'motor': [0, 180], 'screenx': [4, 96], 'screeny': [59, 5]} # screeny is backwards because it is from top to bottom
        #Battery

        super().__init__(width, height, i2c, addr = 0x3C, external_vcc = external_vcc)

  
    def displayscreen(self,whereamI):
        for IconX,IconY,frame in Icons[whereamI]:
            self.blit(frame, IconX, IconY, 0)
        self.show()

    def selector(self,whereamI,icon,previcon):
        if(whereamI==0 or whereamI == 4):
            padding=3
            width=height=iconSize[whereamI]+2*padding
            self.rect(Icons[whereamI][previcon][0]-padding,Icons[whereamI][previcon][1]-padding,width,height, 0) #delete previous selector icon
            self.rect(Icons[whereamI][icon][0]-padding,Icons[whereamI][icon][1]-padding,width,height, 1) #display current selector
            self.displayscreen(whereamI)
        else:
            self.fill_rect(102,29,25,25, 0) #delete previous selector icon
            #self.blit(fb_UP, 102, 0, 0)
            self.blit(fb_upnobox,110,19,0)
            self.blit(Icons[whereamI][icon][2], 102, 29, 0)
            self.blit(fb_downnobox,110,56,0)
            #self.blit(fb_DOWN, 102, 49, 0)
        self.show()
        
    
    def showbattery(self, batterylevel):
        startx=102
        starty=0
        length=20
        width=6
        gap=2
        print(batterylevel)
        #if(batterylevel>3000): #charging
        if(batterylevel=="charging"): #charging
            self.blit(fb_battcharging,startx,starty,0)
        elif(batterylevel=="full"): #full charge
            self.blit(fb_batthigh,startx,starty,0)
        elif(batterylevel=="half"): #medium charge
            self.blit(fb_battmid,startx,starty,0)
        elif(batterylevel=="low"): # low charge
            self.blit(fb_battlow,startx,starty,0)
        else:
            pass
        self.show()
        

    
    def transform(self,initial, final, value):
        initial = self.ranges[initial]
        final = self.ranges[final]
        return int((final[1]-final[0]) / (initial[1]-initial[0]) * (value - initial[0]) + final[0])
    
    def graph(self, oldpoint,point, points):
        rectsize=8
        dotsize=4
        ox,oy=oldpoint
        x,y=point
        ox=self.transform('light', 'screenx', ox)
        oy=self.transform('motor','screeny',oy)
        x=self.transform('light', 'screenx', x)
        y=self.transform('motor','screeny',y)
        
        self.rect(ox-int(rectsize/2),oy-int(rectsize/2),rectsize,rectsize,0)
        self.rect(0,0,100,64,1)
        self.rect(x-int(rectsize/2),y-int(rectsize/2),rectsize,rectsize,1)
        for i in points:
            x,y=i
            x=self.transform('light', 'screenx', x)
            y=self.transform('motor','screeny',y)
            self.fill_rect(x-int(dotsize/2),y-int(dotsize/2),dotsize,dotsize,1)
        self.show()
    
    def cleargraph(self):
        self.fill_rect(1,1,98,62,0)
        self.rect(0,0,100,64,1)

        
    def showmessage(self,msg):
        self.fill(0)
        self.rect(0,20,100,20,0)
        self.text(msg,1,30,1)
        self.show()
        time.sleep(2)
        self.fill(0)
        self.show()
        
        
    def welcomemessage(self):
        self.fill(1)
        self.show()
        
        for a in range(32):
            i=2*a
            self.fill_rect(64-(2*i),32-i,4*i,2*i,0)
            self.blit(fb_SMLOGO,39,7,0)
            self.show()
        '''
        for i in range(80):
            self.fill(0)
            self.blit(fb_SMLOGO,38-i,7,0)
            self.blit(fb_SMLOGO,40+i,7,0)
            self.show()
        '''
        self.clear()
        self.show()
        
    def clear(self):
        self.fill(0)
        self.show()


