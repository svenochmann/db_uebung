#
##Der Abgegebene Code ist nicht Fertig.
#
import machine
import time
from machine import Pin, PWM, Timer, ADC
import math

def sinus_gen():
    return None


class Sampler():
    # Klassenvariablen
    tim = Timer(0)  
    samples = []    
    conv = False   
    

    def __init__(self, fs):
        machine.freq(240000000)  # CPU-Frequenz einstellen
        self.pwm_pin = PWM(Pin(0))  # PWM-Objekt für Pin 0 erstellen (Lautsprecher)
        self.adc = ADC(Pin(34), atten=ADC.ATTN_11DB) 
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


    def convAD(self, T):
        #T Aufnahme zeit in sekunden
        for  i in range(T):
            Sampler.adc.duty_u16()
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
    def startAD(self, T):
        gen = self.convAD(T)

        self.conv = True
        #Converten


if __name__ == "__main__":
    #fs = 5000
    #sampler = Sampler(fs)  # Sampler-Objekt mit Abtastfrequenz 5000 Hz erstellen
    #Aufgabe 4 B:
    #Folgend sollte noch der Code der die Sinus-töne erstellt dies wurde zeitlich nicht mehr geschaft.
    




    #Vorgabe uebung_5
    import gc
    gc.collect()
    print ("Freier Speicher: {0}KiB".format(gc.mem_free()/1024))     
    fs =6000 #sample freq     
    T = 5#record time in sec     
    sampler=Sampler(fs)     
    for wait in range(3,0,-1):         
        print("Sampling starts in {0} seconds...".format(wait))         
        time.sleep(1)   

    sampler.startAD(T)     
    print("Recording...")     
    start_ticks = time.ticks_ms()     
    sampler.startAD(T)     
    while (sampler.conv):
        pass     
    end_ticks = time.ticks_ms()     
    
    print("Sampling after T={0} sec. finished ({1} samples, {2}KiB).".format(time.ticks_diff(end_ticks,start_ticks)/
                                                                             1000,len(Sampler.samples),len(Sampler.samples)*2/1024))         
    #Abspielen des Aufgenommenden
    while True:         
        sampler.startDA()         
        print("Playback...")         
        while (sampler.conv):pass         
        print("Done.")         
        time.sleep(2)
    