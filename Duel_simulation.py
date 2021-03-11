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

0- Uninfected
1- Asymptomatic
2- Recovered
3- Symptomatic
4- Dead
"""



count_asympt = 0
count_sympt = 0
#radio.set_group(255)

#curr_st = '0' # Make the device infected here and remove the line next time you connect to the computer 
radio.on()
#final = ""
sleep_time = 5 #Overall broadcast interval

flag = False

##Load the microbit the Dev_id + initial states followed with a comma and flash the device. The curr_st.txt 
##should have something like Adrian : 0,0,0,0,  before flashing the device


with open("curr_st.txt") as f:
        result = f.read()
        print(result)
curr_st = result[-2]
final = result



while True:
    
    radio.send(curr_st)
    # incoming = radio.receive()
    details = radio.receive_full()

    #Progression
    if curr_st == '3':
        count_sympt += 1
        if count_sympt > 3: #This number can be changed
            #curr_st = '4'
            curr_st = str(random.choice([2,4]))

            count_sympt = 0
    if curr_st == '1':
        count_asympt += 1
        if count_asympt > 3:
            #Asymptomatic converts to symptomatic with a 40% chance and recovers with a 60% chance
            curr_st = '3' if random.random() >0.6 else '2'
            count_asympt = 0

    final += curr_st
    if curr_st !='4':
        final += ","
    with open('curr_st.txt', "w") as my_file:
        my_file.write(final)

    if details:
        byte_message, rssi, timestamp = details
        signal = rssi
        incoming = str(byte_message, 'utf8')[-1]
        if signal > -65 and incoming: #between 0 and 6ft

            if curr_st == '0' and (incoming == '1' or incoming=='3'):
                curr_st = '1'
            #Reinfection occurs with a 10% chance for people who have already recovered
            elif curr_st == '2' and (incoming == '1' or incoming =='3'):
                if random.random()>0.9:
                    curr_st = '1'

    else:
        incoming = None
        signal = None

    print("Curr state : ", curr_st)
    print("Incoming state : ", incoming)
    print("Signal strength : ", signal)
    # print("Details : ", details)
    if  curr_st == '3':
        display.show(Image.SAD)
    elif curr_st == '2':
        display.show(Image.ASLEEP)
    elif curr_st == '4':
        display.show(Image.NO)
        flag = True
        break

    else:
        display.show(Image.HAPPY)
    try:
        utime.sleep(sleep_time)
    except:
        pass

    f = open('curr_st.txt')
    print(f.read())
    f.close()



if flag:
    count_incoming_None = 0
    with open('curr_st.txt', "w") as my_file:
        my_file.write(final)
    f = open('curr_st.txt')
    print(f.read())
    f.close()




    while count_incoming_None<5:
        details = radio.receive_full()
        if details:
            byte_message, signal, timestamp = details
            incoming = str(byte_message, 'utf8')[-1]
        else:
            incoming = None
        if incoming:
            count_incoming_None = 0

        else:
            count_incoming_None += 1
        print("Incoming state : ", incoming)
        try:
            utime.sleep(sleep_time)
        except:
            pass
    print("Attempted 5 times, no signal. Exiting...")
