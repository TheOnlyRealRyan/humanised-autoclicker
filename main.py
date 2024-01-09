import pyautogui
from random import uniform
from pynput.keyboard import *
import time

# TODO: Ryanify code
# TODO: select button to include shift/ctrl/alt+hotkey combinations 
#  ======== settings ========
# Delay Settings
startCPS = 6
CPS = 7
startDelay = 1/startCPS
goalDelay = 1/CPS



hotkey = KeyCode.from_char('r')

pause = True
running = True
startSwitch = True


def on_press(key):
    global running, pause
    if pause and key == hotkey:
        startSwitch = True
        pause = False
        print("--> Started")
    elif key == hotkey:
        pause = True
        startSwitch = True
        print("--> Paused")
    else:
        pass
    

def display_controls():
    print("-"*20)
    print("--Settings--")
    print("CPS: ", CPS, "\nDelay: ", round(goalDelay, 4), "sec")
    print("--Controls--")
    print("Hotkey = R")
    print("-"*20)


def RNGLower(delay):
    return delay + round(uniform(0.0001,0.0010), 6)


def RNGHigher(delay):
    return delay - round(uniform(0.0001,0.0010), 6)


def RNGStartHigher(delay):
    return delay - round(uniform(0.01,0.02), 6)


def main():
    newDelay = startDelay
    switch = True
    startSwitch = True
    delayRange = 0.5


    lis = Listener(on_press=on_press)
    lis.start()
    display_controls()
    

    while running:        
        if not pause:
            if startSwitch and switch:
                if 1/newDelay <= CPS:
                    newDelay = RNGStartHigher(newDelay)
                else:
                    newDelay = RNGLower(newDelay)                
                    startSwitch = False
            else:
                if switch:
                    newDelay = RNGHigher(newDelay)
                else:
                    newDelay = RNGLower(newDelay)
                if 1/newDelay >= CPS+delayRange:
                    switch = False
                elif 1/newDelay <= CPS-delayRange: 
                    switch = True
            
            pyautogui.click(pyautogui.position())
            pyautogui.PAUSE = newDelay
            
            # print("Current CPS: ", 1/newDelay)
        else:
            startSwitch = True          
            newDelay = startDelay
            time.sleep(0.1)

    lis.stop()


if __name__ == "__main__":
    main()