"""
You must configure x_pad and y_pad by yourself
"""
from PIL import ImageGrab
from PIL import Image
import os
import time
from ctypes import windll
user32 = windll.user32
user32.SetProcessDPIAware()
from api import Api

## Globals--------
a = Api()
a.setPads()
pads = a.getPads()
x_pad = pads[0]
y_pad = pads[1]


def screenGrab():
    '''
    Takes an image of the play area and saves it the bit heroes directory
    '''
    box = (1+x_pad,1+y_pad,1585+x_pad,1127+y_pad)
    im = ImageGrab.grab(box)
    im.save(os.getcwd()+'\\thisGame__' + str(int(time.time())) + '.png','PNG')


def main():
    screenGrab()
    
if __name__ == '__main__':
    main()
    