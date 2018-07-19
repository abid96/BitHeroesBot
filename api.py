"""
newest version auto configures x and y pad
"""
from PIL import ImageGrab
from PIL import Image
from PIL import ImageOps
from Cord import Cord
from numpy import *
import os
import time
from ctypes import windll
import win32api
import win32con
import win32gui
user32 = windll.user32
user32.SetProcessDPIAware()

class Api:

    def __init__(self):
    
        self.x_pad = 0
        self.y_pad = 0
    
    def leftClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(.1)
        
    def rightClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        time.sleep(.1)
        
    def leftDown(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1) 
    
    def leftUp(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(.1)     
    
    def rightDown(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(.1) 
    
    def rightUp(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(.1) 
    
    def screenGrab(self):
        '''
        Takes an image of the area defined by box, which in
        this case is the entire game area
        '''
        box = (1+self.x_pad,1+self.y_pad,1585+self.x_pad,1127+self.y_pad)
        im = ImageGrab.grab(box)
        #im.save(os.getcwd()+'\\full_snap__' + str(int(time.time())) + '.png','PNG')
        return im
    
    def grab(self,version=None):
        '''
        Takes an image of the area defined by box. Different detection methods
        require differnt boxes and the version allows them to choose their box.
        '''
        if version == 1:
            box = (1+self.x_pad+641,1+self.y_pad+324,1+943+self.x_pad,1+385+self.y_pad) #dungeon clear
        elif version == 2:
            box = (1+self.x_pad+451,1+self.y_pad+388,1+1141+self.x_pad,1+763+self.y_pad)
        elif version == 3:
            box = (1+self.x_pad+479,1+self.y_pad+459,1+1095+self.x_pad,1+683+self.y_pad) #defeat
        elif version == 4: #GvG victory
            box = (1+self.x_pad+530,1+self.y_pad+158,1+1049+self.x_pad,1+263+self.y_pad)
        else:
            raise(ValueError('Invalid Version Number for Grab'))
        
        
        im = ImageOps.grayscale(ImageGrab.grab(box))
        a = array(im.getcolors())
        
        return sum(a) 
    
    def mousePos(self,cord):
        '''
        Moves mouse to the provided coordinate
        '''
        win32api.SetCursorPos((self.x_pad + cord[0], self.y_pad + cord[1]))
    
    def get_cords(self):
        '''
        Prints the coordinates of your mouse
        '''
        x,y = win32api.GetCursorPos()
        x = x - self.x_pad
        y = y - self.y_pad
        print((x,y))
    
    def getPads(self):
        return (self.x_pad,self.y_pad)
    def reconnected(self):
        '''
        If the reconnect screen isn't there, it will return true
        otherwise it will just reconnect. 
        '''
        b = self.screenGrab()
        neededRGBVal = (21, 149, 180)
        gottenRGBVal = b.getpixel((794,799))        
        
        if neededRGBVal != gottenRGBVal:
            return True
        else:
            if 290965 == self.grab(2):
                # Press Reconnect
                self.mousePos(Cord.u_reconnect)
                time.sleep(.1)
                self.leftClick()
                time.sleep(.1)
                
                # Move Mouse out of way
                self.mousePos(Cord.u_outOfWay)
                time.sleep(5)
            else:
                return True

    def detectHomeScreen(self):
        im = self.screenGrab()
        neededRGBValList = [(0, 142, 215),(198, 147, 10),(154, 238, 41),(188, 20, 55)]
        gottenRGBValList = []
        
        gottenRGBValList.append(im.getpixel((217, 46)))
        gottenRGBValList.append(im.getpixel((527, 42)))
        gottenRGBValList.append(im.getpixel((831, 36)))
        gottenRGBValList.append(im.getpixel((1144, 51)))
        
        return neededRGBValList == gottenRGBValList 
        
    def getBitHeroesWindow(self):
        '''
        returns the hwnd that is the bit heroes window
        ''' 
        windowWeWant = []
        def enumHandler(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                if 'Bit Heroes' == win32gui.GetWindowText(hwnd):
                    windowWeWant.append(hwnd)
        win32gui.EnumWindows(enumHandler, None)
        return windowWeWant[0]    
    
    def setPads(self):
        '''
        sets the correct value for x and y pads
        '''
        bitHeroes = self.getBitHeroesWindow()
        coord = win32gui.GetWindowRect(bitHeroes)
        self.x_pad = coord[0] + 7 
        self.y_pad = coord[1] + 65
    def main(self):
        pass
        #screenGrab()
    
    
if __name__ == '__main__':
    #pass
    a = Api()
    a.setPads()


    #print(a.grab(4))
    #im = a.screenGrab()
    #print(im.getpixel((217, 46)))
    #print(im.getpixel((527, 42)))
    #print(im.getpixel((831, 36)))
    #print(im.getpixel((1144, 51)))
    
    #print(a.get_cords())
    #print(a.reconnected())
    print(a.detectHomeScreen())