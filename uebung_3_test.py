import machine
import time
from machine import Pin
from machine import PWM
from machine import Timer
from machine import ADC
import math


class Sampler():
#class variables
    tim = Timer(0)
    samples = []
    conv = False
#Your code is starting here
    def __init__(self, fs):
        machine.freq(240000000)
        Sampler.pwm_pin.init(int(1E5), duty_u16=32768)
        time.sleep_ms(50)
        self.fs = fs
#Your code is starting here
    def pwm(self, duty):
    '''
    Starts pwm signal.
    duty : duty-cycle in [0,65535]
    '''
        if (duty < 0) or (duty > 65535):
            raise Exception("Duty-Cycle must be in between [0,65535]%!")
        
    
    
    
    
def convDA(self): # Convertion Digital to Analog
    for duty in Sampler.samples:
        

    yield
    
    
    
    def handler(self,gen):
        try:
            next(gen)
        except StopIteration:
            Sampler.tim.deinit()
            self.conv = False
    def startDA(self):
        gen = self.convDA()
        self.conv = True
        Sampler.tim.init(mode=Timer.PERIODIC, freq=self.fs, callback=lambda
        t:self.handler(gen))#Your code starting here