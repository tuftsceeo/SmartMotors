from machine import Pin, ADC
from neopixel import NeoPixel
import time
import build_rainbow
import micropython

class SmartLight:
    def __init__(self, neo_pin, resolution=700):
        self.np = NeoPixel(Pin(neo_pin, Pin.OUT), 12)
        self.resolution = resolution
        self.colors = self.build_rainbow(self.resolution)
        self.resolution = len(self.colors)-1   # get the actual number of colors, differs from desired due to rounding
        self.cycling_color = True     # if false, cycling brightness
        
        self.color = [255, 0, 0]
        self.brightness = 100        # brightness values from 0 to 100
        self.num_leds = 12
        self.LED = [255, 0, 0]     # led value which combines color and brightness
        
        self.parameters = ['color', 'brightness', 'number']
        self.param_num = 0
        self.parameter = self.parameters[self.param_num]
        
        
    def build_rainbow(self, resolution):
        rainbow = []
        num = int(255/(resolution/3))
        
        for i in range(0, 255, num):
            rainbow.append((255-i, i, 0))           
        for i in range(0, 255, num):
            rainbow.append((0, 255-i, i))           
        for i in range(0, 255, num):
            rainbow.append((i, 0, 255-i))
            
        return rainbow
    
    def switch_parameter(self):
        self.param_num = ((self.param_num + 1)%len(self.parameters))-1
        self.get_parameter()
        if (self.parameter != 'color'):
            self.color = [255, 255, 255]
        print('training ' + str(self.get_parameter()))
        
    def train_brightness(self):
        self.parameter = 'brightness'
        self.param_num = 1
        print(self.parameter)
        
    def train_num_leds(self):
        self.parameter = 'number'
        self.param_num = 2
        print(self.parameter)
        
    def train_color(self):
        self.parameter = 'color'
        self.param_num = 0
        print(self.parameter)
        
    def get_LED(self):
        for i in range(3):
            self.LED[i] = int(self.color[i] * (self.brightness / 100))      # set LED value to determined color and brightness
        return(self.LED)
    
    def write_LED(self, value):
        self.color = self.colors[value]
        for i in range(self.num_leds):
            self.np[i] = tuple(self.color)    # set each LED value
        self.np.write()
        
    def get_resolution(self):
        '''returns length of colors array'''
        return self.resolution
    
    def get_parameter(self):
        self.parameter = self.parameters[self.param_num]
        return self.parameter
    
    def set_color(self, color):
        self.color = self.colors[color]
        
    def set_brightness(self, b):
        self.brightness = b
        
    def set_num_leds(self, num):
        self.num_leds = num
