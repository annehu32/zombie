from Tufts_ble import Sniff, Yell
import uasyncio as asyncio
from machine import Pin, PWM
import time
import neopixel

# ----------------- PIN ASSIGNMENTS ------------------------------
# defining pins that we'll be needing...
# want 3 indicator lights, buzzer, neopixel to indiciate state
buzzer = PWM(Pin('GPIO18', Pin.OUT))  # buzzer
neo = neopixel.NeoPixel(Pin(28), 1)   # neopixel
firstHit = Pin('GPIO1', Pin.OUT)
secondHit = Pin('GPIO5', Pin.OUT)
thirdHit = Pin('GPIO9', Pin.OUT)

#----------------- BLUETOOTH FUNCTIONS -----------------------
async def zombie(): # Peripheral yells - zombie function
    state = (0,10,0)  # Zombie = green
    neo[0] = state
    neo.write()
    p = Yell()
    while True:    # Zombie will yell and yell and yell
        p.advertise(f'!2')
        print('in zombie loop')
        await asyncio.sleep(0.1)

# ----------------- MAIN CODE ------------------------------
# Main function will run sequentially
async def main():   
     zombie() # Zombie function will only stop via keyboard interrupt
                    # maybe we want to add an external button to stop?

# Setting up the asyncio event loop
loop = asyncio.get_event_loop()
print('loop created')
loop.create_event(zombie())

