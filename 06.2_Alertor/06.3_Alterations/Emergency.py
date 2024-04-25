from gpiozero import TonalBuzzer, Button, PWMLED
import time
from signal import pause

BUZZER = TonalBuzzer(17)
BUTTON = Button(18)
LED = PWMLED(13)

HIGH_TONE = 600 # The max is 880 but that hurts my ears
LOW_TONE = 220
    
def setup():
    # Setup events for when the button is pressed and released
    BUTTON.when_pressed = alertor and loop
    
    BUTTON.when_released = stop_alertor
    
def loop():
    while True:
        i : int = 0
        # range() only works with integers
        for i in range(0, 10):
            # led.value only accepts floats
            LED.value = i / 10
            time.sleep(0.1)
            
        for i in range(10, 0, -1):
            LED.value = i / 10
            time.sleep(0.1)
            
def alertor():
    print ('alertor turned on >>> ')
    
    while True:  
        # Linear
        for x in range(LOW_TONE, HIGH_TONE):
            BUZZER.play(x)
            time.sleep(0.002)
            
            if not BUTTON.is_pressed:
                return  
            
        for x in range(HIGH_TONE, LOW_TONE, -1):
            BUZZER.play(x)
            time.sleep(0.002)
            
            if not BUTTON.is_pressed:
                return 
            

        
def stop_alertor():
    BUZZER.stop()
    print ('alertor turned off <<<')

def destroy():
    BUZZER.close()
    BUTTON.close()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        pause()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
