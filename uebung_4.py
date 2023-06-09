#
##Der Abgegebene Code ist nicht Fertig.
#
import machine
import time
from machine import Pin, PWM, Timer
import math

class Sampler():
    # Klassenvariablen
    tim = Timer(0)  
    samples = []    
    conv = False    

    def __init__(self, fs):
        machine.freq(240000000)  # CPU-Frequenz einstellen
        self.pwm_pin = PWM(Pin(0))  # PWM-Objekt für Pin 0 erstellen (Lautsprecher)
        time.sleep_ms(50)   
        self.fs = fs         # Abtastfrequenz festlegen

    def pwm(self, duty):
        '''
        Startet das PWM-Signal.
        duty : Duty-Zyklus in [0, 65535]
        '''
        if (duty < 0) or (duty > 65535):
            raise Exception("Duty-Cycle must be in between [0, 65535]!")
        self.pwm_pin.duty_u16(duty)  # Duty für das PWM-Signal einstellen

    def convDA(self):
        for duty in Sampler.samples:
            Sampler.pwm_pin.duty_u16(duty)  # Duty für das PWM-Signal einstellen
            yield  

    def handler(self, gen):
        try:
            next(gen)  # Nächstes Sample aus dem Generator abrufen
        except StopIteration:
            Sampler.tim.deinit()  # Timer deaktivieren, wenn alle Samples verarbeitet wurden
            self.conv = False   

    def startDA(self):
        gen = self.convDA()  # Generator für die Konvertierung erstellen
        self.conv = True
        Sampler.tim.init(mode=Timer.PERIODIC, freq=self.fs, callback=lambda t: self.handler(gen))
        # Timer initialisieren: periodischer Modus, Frequenz fs, Callback-Funktion verwenden

if __name__ == "__main__":
    sampler = Sampler(5000)  # Sampler-Objekt mit Abtastfrequenz 5000 Hz erstellen
    #Aufgabe 4 B:
    #Folgend sollte noch der Code der die Sinus-töne erstellt dies wurde zeitlich nicht mehr geschaft.
    