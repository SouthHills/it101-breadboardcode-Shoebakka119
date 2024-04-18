# NOTE: If this fails to run, turn off the SPI and I2C interfaces.
# Turn them back on when this lab is complete.
# Alternatively, you can use the lesser abstracted RPi.GPIO interface
#   in the LightWater_RPi.GPIO.py file.
from gpiozero import LEDBarGraph
from time import sleep

LED_PINS : list[int] = [17, 18, 27, 22, 23, 24, 25, 2, 3, 8]
LEDS = LEDBarGraph(*LED_PINS, active_high=False)

def setup():
    global LEDS
    for led in LEDS:  # make led(on) move from left to right
        led.off()

def loop():
    global LEDS
    while True:
        for pin in ledPins:     # make led(on) move from left to right
            GPIO.output(pin, GPIO.HIGH)  
            time.sleep(0.1)
            GPIO.output(pin, GPIO.LOW)
        for pin in ledPins[::-1]:       # make led(on) move from right to left
            GPIO.output(pin, GPIO.HIGH)  
            time.sleep(0.1)
            GPIO.output(pin, GPIO.LOW)

def destroy():
    global LEDS
    for led in LEDS:  # make led(on) move from left to right
        led.close()

if __name__ == '__main__':  # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
