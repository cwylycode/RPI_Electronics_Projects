"""
This project allows morse code to be signaled through an LED and an active buzzer, allowing you to see and hear the morse encoded stuff you write!

A module dependency is needed to convert text into morse code. This module is a single script and can be found here: https://github.com/hexadeci-male/dumptruck/blob/main/python/morse.py

Required parts:
- RPI 40-pin GPIO
- Breadboard
- LED
- Active Buzzer
- Wires and resistors
"""

from morse import morse_encode # Put morse script in same directory as this script
from gpiozero import LED,Buzzer # Comes with the RaspberryPi
from time import sleep
import os

# Morse code writing speeds. A unit defines all other speeds. Lower unit value = quicker writing.
unit = 50/1000 # Time length of one message element (arbitrary, usually 10-100 milliseconds)
speed_dot = unit # Length of a dot/dit (officially, 1 unit)
speed_dash = unit*3 # Length of a dash/dah (officially, 3 units)
speed_intra = unit # Length of gap between dots and dashes inside a character (officially, 1 unit)
speed_char = unit*3 # Length of gap between characters (officially, 3 units)
speed_word = unit*7 # Length of gap between words (officially, 7 units)

# RPI pin setup for LED and Buzzer
led = LED(4)
buzzer = Buzzer(17)

def clear_screen():
    os.system("cls" if os.name == 'nt' else "clear")

def prompt_config():
    clear_screen()
    config_txt = """
    Would you like to use light, sound, or both for signaling your message?

    1) Both (Default)
    2) Light Only
    3) Sound Only

    Type in a number, then press 'Enter'
    > """
    usr = input(config_txt)
    try:
        i = int(usr)
        if 0<i<4: return i
        elif i == 0: return 0 # Debugging purposes - no gpio
        else: return 1
    except:
        return 1

def prompt_message():
    clear_screen()
    info_txt = """
    Type in a message and have it converted to Morse code.
    All ASCII (32-126) chars are accepted with the exceptions of: ~ ` # % ^ * { } [ ] < > \\ |
    Invalid characters will be blanked out.

    Type in your message, then press 'Enter'
    > """
    return input(info_txt).upper()

def prompt_repeats():
    clear_screen()
    length_txt = """
    How many times should the message repeat? Once is the default.

    Type in a number.
    > """
    usr = input(length_txt)
    try:
        i = int(usr)
        if i>0: return i
    except:
        return 1

def signal_morse(code:str,txt:str,remaining:int,gpio_config:int):
    clear_screen()
    info = f"""
    Signaling message in Morse code. Press 'ctrl + c' to exit program.
    Remaining Loops: {remaining}
    \n"""
    print(info)
    i,max = -1,len(code)
    for c in txt:
        while True:
            i+=1
            if code[i] == ' ':
                continue
            elif code[i] in ['/','*']:
                print(' ',end='',flush=True)
                sleep(speed_word)
                break
            else:
                print(c,end='',flush=True)
                while i<max:
                    if code[i] == '.':
                        activate_gpio(gpio_config,speed_dot)
                    elif code[i] == '-':
                        activate_gpio(gpio_config,speed_dash)
                    else:
                        break
                    i+=1
                    sleep(speed_intra)
                sleep(speed_char)
                break

def activate_gpio(cfg_val:int,duration:int):
    if cfg_val == 1:
        led.on()
        buzzer.on()
        sleep(duration)
        led.off()
        buzzer.off()
    elif cfg_val == 2:
        led.on()
        sleep(duration)
        led.off()
    elif cfg_val == 3:
        buzzer.on()
        sleep(duration)
        buzzer.off()
    else: sleep(duration)

# Main Program
def app():
    cfg_num = prompt_config()
    while True:
        msg_txt = prompt_message()
        msg_loops = prompt_repeats()

        msg_code = morse_encode(msg_txt)
        for count in range(msg_loops):
            signal_morse(msg_code,msg_txt,msg_loops-count-1,cfg_num)
            sleep(1)

        print("\n\nDone.")
        sleep(3)

# Execute
if __name__ == "__main__":
    try: app()
    #Auto-cleanup of gpio
    except Exception as e: print(e)