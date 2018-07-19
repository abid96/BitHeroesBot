'''
This is a part of a program to play the game bit heroes.
This module in particular is responsible for farming raids
until the resources end.

v1.0

- Abid Rizvi
'''

from PIL import Image
import time
from api import Api
from Cord import Cord
import time

class RaidCrawler:
    
    def __init__(self):
        self.api = Api()
        self.api.setPads()
        self.resources = 4
        
        while not self.api.detectHomeScreen():
            self.api.reconnected()
            time.sleep(1)
        
    def _clickRaid(self):
        '''
        Clicks the quest button on the main menu
        '''
        self.api.mousePos(Cord.mm_raid)
        self.api.leftClick()    
    
    def _chooseLevel(self,raid,difficulty):
        '''
        after clicking the quest button, this method
        will then choose the zone, dungeon, difficulty 
        and then click start
        '''
        # Clicking quest button
        self._clickRaid()
        time.sleep(.5)
        
        # Choosing the appropriate raid
        if raid == 1:
            # Choosing the raid
            self.api.mousePos(Cord.r_1)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)             
        elif raid == 2: 
            # Choosing the raid
            self.api.mousePos(Cord.r_2)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)    
        else:
            raise ValueError('Undefined Raid Choice')   

        # Hitting the summon button
        self.api.mousePos(Cord.r_summon)
        time.sleep(.1)
        self.api.leftClick()
        time.sleep(.4)           
        
        # Choosing Difficulty
        if difficulty == 1:
            self.api.mousePos(Cord.u_normal)
            time.sleep(.4)
            self.api.leftClick()
            time.sleep(.1) 
        elif difficulty == 2:
            self.api.mousePos(Cord.u_hard)
            time.sleep(.4)
            self.api.leftClick()
            time.sleep(.1) 
        elif difficulty == 3:
            self.api.mousePos(Cord.u_heroic)
            time.sleep(.4)
            self.api.leftClick()
            time.sleep(.1) 
        else:
            raise ValueError('Undefined Difficulty')
        
        self.api.mousePos(Cord.u_teamAccept)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)
        
        # Move Mouse out of way
        self.api.mousePos(Cord.u_outOfWay)   
    
    def detectFamiliarScreen(self):
        '''
        detects if a familiar has been found. returns boolean
        '''
        pixelCoordVerifyList = [(270,713),(464,943),(852,949),(1086,718)]
        pixelRGBVerifyList = [(55, 176, 208),(240, 100, 108),(241, 136, 41),(155, 208, 30)]
        
        s = self.api.screenGrab()
        rgbValues = []
        for coord in pixelCoordVerifyList:
            rgbValues.append(s.getpixel(coord))
        
        return rgbValues == pixelRGBVerifyList
    
    def detectRaidVictory(self):
        '''
        detects if the raid has been cleared. returns boolean
        '''
        a = self.api.grab(1)
        
        # This segment is needed to avoid similar looking screens.
        # This one specifically makes the item screen not pass as victory
        b = self.api.screenGrab()
        neededRGBVal = (165, 211, 56)
        gottenRGBVal = b.getpixel((745,764))
        
        c = self.api.screenGrab()
        unwantedRGBVal = (153, 0, 255)
        gottenRGBVal2  = c.getpixel((1051,577))
        
        if neededRGBVal != gottenRGBVal:
            return False
        elif unwantedRGBVal == gottenRGBVal2:
            return False
        else:
            return a == 50554      
    def detectDefeat(self):
        '''
        detects if we have been defeated, returns boolean
        '''
        a = self.api.grab(3)
        
        b = self.api.screenGrab()
        neededRGBVal = (55, 179, 211)
        gottenRGBVal = b.getpixel((704,762))
        
        if neededRGBVal != gottenRGBVal:
            return False
        else:
            return a == 169839               
    def eventHandle(self):
        '''
        this will look for familiar detection and victory detection.
        it will handle both those events. upon victory, it will put 
        us back to the home menu. 
        '''
        while not self.detectRaidVictory(): #and self.detectDefeat():
            if self.detectFamiliarScreen():
                print('Familiar Detected!')
                
                # Persuading the familiar
                time.sleep(.1)
                self.api.mousePos(Cord.f_persuade)
                time.sleep(.1)
                self.api.leftClick()
                time.sleep(.4) 
                self.api.mousePos(Cord.f_confirm)
                self.api.leftClick()
                self.api.mousePos(Cord.u_outOfWay)
                time.sleep(.4)
        
        if self.detectRaidVictory():
            print('Victory!') 
                  
            # Exiting Raid
            time.sleep(.4)
            self.api.mousePos(Cord.q_victExit) # is for dungeons but works here too
            time.sleep(.4)
            self.api.leftClick()
            time.sleep(3.5)  
        else:
            print('Defeat...')
            
            # Exiting Raid
            time.sleep(.4)
            self.api.mousePos(Cord.u_defeatClose) # is for dungeons but works here too
            time.sleep(.4)
            self.api.leftClick()
            time.sleep(3.5)  
            
        # Returning to the main menu
        self.api.mousePos(Cord.r_menuExit)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)
        
        # Put mouse out of the way
        self.api.mousePos(Cord.u_outOfWay) 
    
    def setResources(self,amount):
        self.resources = amount    
    def main(self,raid,difficulty):
        '''
        Keeps running the specified raid till resources
        are finished.
        '''
        while self.resources > 0:
            self._chooseLevel(raid,difficulty)
            self.eventHandle()
            time.sleep(2)
            self.resources -= 1
        print('Raid Farm Finished!')
if __name__ == '__main__':
    pass
    #d = RaidCrawler()
    #d.main(1,3) #Raid,difficulty