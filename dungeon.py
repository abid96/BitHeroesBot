'''
This is a part of a program to play the game bit heroes.
This module in particular is responsible for farming quests
until the resources end.

v1.0

- Abid Rizvi
'''

from PIL import Image
import time
from api import Api
from Cord import Cord
import time

class DungeonCrawler:
    
    def __init__(self):
        '''
        The api module provides necessary functions for farming
        The only other global variable we need to watch are resources
        '''
        self.api = Api()
        self.api.setPads()
        self.resources = 172
        
        while not self.api.detectHomeScreen():
            self.api.reconnected()
            time.sleep(1)
    def _clickQuest(self):
        '''
        Clicks the quest button on the main menu
        '''
        self.api.mousePos(Cord.mm_quest)
        self.api.leftClick()
    def _chooseLevel(self,zone,dungeon,difficulty):
        '''
        after clicking the quest button, this method
        will then choose the zone, dungeon, difficulty 
        and then click start
        '''
        # Clicking quest button
        self._clickQuest()
        time.sleep(.5)
        
        # Press Zone Menu
        self.api.mousePos(Cord.q_zoneMenu)
        time.sleep(.1)
        self.api.leftClick()
        time.sleep(.1) 
        
        # Move to scroll button
        self.api.mousePos(Cord.q_zMenuScrollUp)
        time.sleep(.1)
        
        # Wake up the scroll button
        self.api.leftDown()
        time.sleep(.1)
        self.api.leftUp()
        time.sleep(.1)
        
        # Press scroll button to adjust menu
        self.api.leftDown()
        time.sleep(2)
        self.api.leftUp()
        time.sleep(.1)
        
        # Choosing the appropriate zone and dungeon
        if zone == 1:
            # Choosing the zone
            self.api.mousePos(Cord.q_zMenu1)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)   
            
            # Exit button Hit in case zone is already chosen
            self.api.mousePos(Cord.q_zMenuExit)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)            
            
            # Choosing the dungeon
            if dungeon == 1:
                self.api.mousePos(Cord.q_z1d1)
                time.sleep(.3)
                self.api.leftClick()
                time.sleep(.1)        
            else:
                raise ValueError('Undefined Dungeon Choice')            
        elif zone == 4:
            
            # Choosing the zone
            self.api.mousePos(Cord.q_zMenu4)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)   
            
            # Exit button Hit in case zone is already chosen
            self.api.mousePos(Cord.q_zMenuExit)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)            
            
            # Choosing the dungeon
            if dungeon == 3:
                self.api.mousePos(Cord.q_z4d3)
                time.sleep(.3)
                self.api.leftClick()
                time.sleep(.1)        
            else:
                raise ValueError('Undefined Dungeon Choice')
        else:
            raise ValueError('Undefined Zone Choice')   

        
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
    
    def detectDungeonVictory(self):
        '''
        detects if the dungeon has been cleared. returns boolean
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
        while not self.detectDungeonVictory() and not self.detectDefeat():
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
        
        if self.detectDungeonVictory():
            print('Victory!') 
                  
            # Exiting Dungeon
            time.sleep(.4)
            self.api.mousePos(Cord.q_victExit)
            time.sleep(.4)
            self.api.leftClick()
            time.sleep(3.5)
        else:
            print('Defeat...')
            # Exiting Dungeon
            time.sleep(.4)
            self.api.mousePos(Cord.u_defeatClose)
            time.sleep(.4)
            self.api.leftClick()
            time.sleep(3.5)            
        
        # Returning to the main menu
        self.api.mousePos(Cord.q_menuExit)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)
        
        # Put mouse out of the way
        self.api.mousePos(Cord.u_outOfWay)
    
    def setResources(self,amount):
        self.resources = amount
    
    def main(self,zone,dungeon,difficulty):
        '''
        Keeps running the specified dungeon till resources
        are finished.
        '''
        if difficulty == 1:
            while self.resources >= 10:
                self._chooseLevel(zone,dungeon,difficulty)
                self.eventHandle()
                time.sleep(2)
                self.resources -= 10
            
        elif difficulty == 2:
            while self.resources >= 20:
                self._chooseLevel(zone,dungeon,difficulty)
                self.eventHandle()
                time.sleep(2)
                self.resources -= 20
            
        elif difficulty == 3:
            while self.resources >= 30:
                self._chooseLevel(zone,dungeon,difficulty)
                self.eventHandle()
                time.sleep(2)
                self.resources -= 30
        
        print('Dungeon Farm Finished!')            
if __name__ == '__main__':
    pass
    #d = DungeonCrawler()
    #d.main(4,3,1) #Zone,dungeon,difficulty
    #d.eventHandle()
    #print(d.detectDefeat())
    
    
    
    
   