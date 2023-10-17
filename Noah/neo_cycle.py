from machine import Pin, ADC
from neopixel import NeoPixel
import time
import build_rainbow
import micropython

micropython.alloc_emergency_exception_buf(100) # allows error reporting for callbacks

pot_pin = 3
button_pin = 9
neo_pin = 2

pot = ADC(Pin(pot_pin))        # set up potentiometer with analog pin
pot.atten(ADC.ATTN_11DB)       # full range: 3.3v

button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)    # set button pin to input to switch cycle type
#button = ADC(Pin(button_pin))

neo = Pin(neo_pin, Pin.OUT)   # set neo_pin to output to drive NeoPixels
np = NeoPixel(neo, 12)   # create NeoPixel driver on GPIO0 for 12 pixels

resolution = 700         # desired number of colors
colors = build_rainbow.build_rainbow(resolution)
resolution = len(colors)-1   # get the actual number of colors, differs from desired due to rounding
print(resolution)
cycling_color = True     # if false, cycling brightness

color = [255, 0, 0]
brightness = 1        # brightness values from 0 to 1
LED = [255, 0, 0]     # led value which combines color and brightness

def switch_cycle(change):
    button.irq(handler=None)   # end interrupt to prevent double switching
    global cycling_color
    cycling_color = not cycling_color
    if cycling_color: print("adjust color")
    else: print("adjust brightness")
    time.sleep(0.2)
    button.irq(handler=switch_cycle, trigger=Pin.IRQ_FALLING) #restart intterupt

button.irq(handler=switch_cycle, trigger=Pin.IRQ_FALLING)   # set up button interrupt to switch cycle type

while True:
    pot_value = pot.read()                        # determine color from potentiometer
    if cycling_color:
        color = colors[int((pot_value / 4095) * resolution)]    # scale pot reading to length of color list
    else:
        brightness = pot_value / 4095          # determine brightness from potentiometer
    
    for i in range(3):
        LED[i] = int(color[i] * brightness)      # set LED value to determined color and brightness
        
    for i in range(12):
        np[i] = tuple(LED)    # set each LED value
    #print(LED)
    #print(button.value())
    np.write()
    time.sleep(0.1)