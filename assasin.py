# Add your Python code here. E.g.
import microbit
from microbit import *
import radio
import random
import time
import utime
import os
from sys import exit

"""
Algorithm -
Players attempt to “kill” other players by touching them with a pretend weapon.
There are 'n' microbits and the weapon is how close you get to other microbit
Players get assigned specific individuals to hunt, and are assigned to hunt that player’s target if they successfully take them out? Should we?

0 - dead
1 - alive
Everyone is alive in the beginning
"""

radio.on()
curr_st = '1'

while True:
    
    radio.send(curr_st)
    # incoming = radio.receive()
    details = radio.receive_full()
    
    if curr_st == '0'
        display.show(Image.SAD)
    
    if curr_st == '1':
        display.show(Image.HAPPY) 
    if details:
        byte_message, rssi, timestamp = details
        signal = rssi
        incoming = str(byte_message, 'utf8')[-1]
        if signal > -65 and incoming: #between 0 and 6ft
        ## Implement your logic to kill the microbit something like--
        ##--Press a button and send '0' as current state to other microbit to kill it
        ## Or maybe a probability engine to determine which microbit dies
            if curr_st == '1' and incoming == '1':
                curr_st = '0'

    else:
        incoming = None
        signal = None
        display.show(Image.SAD)

    print("Curr state : ", curr_st)
    print("Incoming state : ", incoming)
    print("Signal strength : ", signal)
