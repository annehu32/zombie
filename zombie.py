from Tufts_ble import Sniff, Yell
import uasyncio as asyncio
from machine import Pin, PWM
import time
import neopixel

# ----------------- PIN ASSIGNMENTS ------------------------------
# defining pins that we'll be needing...
buzzer = PWM(Pin('GPIO18', Pin.OUT))  # buzzer
neo = neopixel.NeoPixel(Pin(28), 1)   # neopixel
button = Pin('GPIO20',Pin.IN) # on-board button

yell = True # As a default, we want the zombie buzzer to make sound

#-----------------  FUNCTIONS -----------------------
# If a button is pressed, readPress What happens when the "pressed" boolean is true
async def toggleButton():
    global yell
    if yell:
        print('----- in button.toggleButton, turning yelling OFF ------')
        yell = False

    else:
        print('----- in button.toggleButton, turning yelling ON ------')
        yell = True

async def readPress():
    print('-----handle_button called -------')
    while True:
        if button.value() != 1:
            time.sleep(0.1)
            if button.value() != 1:
                await toggleButton()
        await asyncio.sleep(0.01)

async def scream():
    global buzzer
    global yell
    
    if yell:
        buzzer.freq(440)
        buzzer.duty_u16(1000)
        await asyncio.sleep(0.1)
        buzzer.duty_u16(0)


async def zombie(): # Peripheral yells - zombie function
    global neo
    state = (0,10,0)  # Zombie = green
    neo[0] = state
    neo.write()
    p = Yell()
    while True:    # Zombie will yell and yell and yell
        p.advertise(f'!2')
        print('in zombie loop')
        await scream()
        await asyncio.sleep(0.1)

# ----------------- MAIN CODE ------------------------------
# Setting up the asyncio event loop
loop = asyncio.get_event_loop()

loop.create_task(zombie())
loop.create_task(readPress())
loop.run_forever()
