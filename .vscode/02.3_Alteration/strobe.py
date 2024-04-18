from gpiozero import LED as LEDClass, Button
from signal import pause
import time

LED = LEDClass(17)  # define ledPin
BUTTON = Button(18)  # define buttonPin
is_blinking = False

def Flipblinking():
    global is_blinking
    is_blinking = not is_blinking



def changeLedState():
    global LED, is_blinking
    if is_blinking == True:
        LED.on()
        time.sleep(.5)
        LED.off()
        time.sleep(.5)
    


def destroy():
    global LED, BUTTON
    LED.close()
    BUTTON.close()

if __name__ == "__main__":
    print ("Program is starting...")
    try:
        BUTTON.when_pressed = Flipblinking
        while True:
            changeLedState()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        



