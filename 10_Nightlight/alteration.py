from pathlib import Path
import sys
import RPi.GPIO as GPIO
import time
from gpiozero import LEDBarGraph


HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

LED_PINS : list[int] = [21, 20, 16, 12, 25, 24, 23, 18, 13, 19]
LEDS = LEDBarGraph(*LED_PINS, active_high=False)
ADC = ADCDevice() # Define an ADCDevice class object


def setup():
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(LED_PINS, GPIO.OUT)   # set all LED_PINS to OUTPUT mode
    GPIO.output(LED_PINS, GPIO.HIGH) # make all LED_PINS output HIGH level, turn off all led


def graph():
    while True:
            for pin in LED_PINS:     # make led(on) move from left to right
                GPIO.output(pin, GPIO.LOW)  
                time.sleep(0.1)
                GPIO.output(pin, GPIO.HIGH)
            for pin in LED_PINS[::-1]:       # make led(on) move from right to left
                GPIO.output(pin, GPIO.LOW)  
                time.sleep(0.1)
                GPIO.output(pin, GPIO.HIGH)
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
        LEDS.value = value / 10   # Mapping to PWM duty cycle        
        voltage = value / 10 * 3.3
        print (f'ADC Value: {value} \tVoltage: {voltage:.2f} \tLED Value: {LEDS.value:.2f}')
        time.sleep(0.01)
        graph()

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