from pathlib import Path
import sys
import RPi.GPIO as GPIO
import time
from gpiozero import LEDBarGraph


HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

LEDS = LEDBarGraph(21, 20, 16, 12, 25, 24, 23, 18, 13, 19)
ADC = ADCDevice() # Define an ADCDevice class object


def setup():
    global ADC
    if(ADC.detectI2C(0x48) and USING_GRAVITECH_ADC): 
        ADC = GravitechADC()
    elif(ADC.detectI2C(0x48)): # Detect the pcf8591.
        ADC = PCF8591()
    elif(ADC.detectI2C(0x4b)): # Detect the ads7830
        ADC = ADS7830()
    else:
        print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
        exit(-1)

def loop():
    global ADC, LEDS
    while True:
        value = ADC.analogRead(0)   # read the ADC value of channel 0
        LEDS.value = value / 255/10   # Mapping to PWM duty cycle        
        voltage = value / 255 * 3.3
        print (f'ADC Value: {value} \tVoltage: {voltage:.2f} \tLED Value: {LEDS.value:.2f}')
        time.sleep(0.01)  
    
        for i in range(1,10):     # make led(on)move from left to right
            if 255/10 * i > value: 
                LEDS[i].off()
            else:
                LEDS [i].on()
                
            
                
    

def destroy():
    global ADC, LEDS
    ADC.close()
    LEDS.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()