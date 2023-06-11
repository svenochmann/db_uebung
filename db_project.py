import machine
import time
from machine import Pin, PWM, Timer, ADC
import math
import gc

# region Sampler

class Sampler:
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
            self.pwm_pin.duty_u16(duty)  # Duty für das PWM-Signal einstellen
            yield  


    def convAD(self, T):
        #T Aufnahme zeit in sekunden
                
        st = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(),st) <(T*1000):
            value=self.adc.read()
            Sampler.samples.append(value)
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
        Sampler.tim.init(mode=Timer.PERIODIC, freq=self.fs, callback=lambda t: self.handler(gen))
        #Converten NICHT FERTIG
# endregion



# region Main
def sinus_sound(fs, freq, amp, dur):
    #Aufgabe 4 B:
    #Erstellt ein Sinus Signal
    #Return Sample liste die eine Sinuscurve wiederspiegelt
    sample_list  = []
    num_samples = int(fs * dur)
    
    for i in range(num_samples):
        sample = int(amp * math.sin(2 * math.pi * freq * i / fs) + amp)
        sample_list.append(sample)
    return sample_list



def uebung_5(fs, T):
    gc.collect()
    print ("Freier Speicher: {0}KiB".format(gc.mem_free()/1024))     
    sampler=Sampler(fs)     
    for wait in range(3,0,-1):         
        print("Sampling starts in {0} seconds...".format(wait))         
        time.sleep(1)   

    #sampler.startAD(T)     
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
    




if __name__ == "__main__":
    
    
    
    #Aufgabe 4:
    """
    fs = 6000
    sampler = Sampler(fs)
    freq = 100
    amp = 32768
    dur=1
    sample_list=sinus_sound(fs, freq, amp,dur)
    Sampler.samples = sample_list
    sampler.startDA()
    """



    #Aufgabe 5:
    """
    fs = 5000
    T = 3
    uebung_5(fs, T)
    """
#endregion