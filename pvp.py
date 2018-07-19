'''
This is a part of a program to play the game bit heroes.
This module in particular is responsible for farming PVP
until the resources end.

v1.0

- Abid Rizvi
'''

from PIL import Image
import time
from api import Api
from Cord import Cord
import time

class PVPCrawler:
    # NOTE: You must set the difficulty level yourself!!
    def __init__(self):
        '''
        The api module provides necessary functions for farming
        The only other global variable we need to watch are resources
        '''
        self.api = Api()
        self.resources = 10
    def _clickQuest(self):
        '''
        Clicks the quest button on the main menu
        '''
        self.api.mousePos(Cord.mm_pvp)
        self.api.leftClick()
    def _chooseTickets(self,tickets):
        '''
        after clicking the pvp button, this method
        will then choose the tickets 
        and then click start
        '''
        # Clicking pvp button
        self._clickQuest()
        time.sleep(.5)
        
        # Press ticket Menu
        self.api.mousePos(Cord.p_tMenu)
        time.sleep(.1)
        self.api.leftClick()
        time.sleep(.1) 
        
        
        # Choosing the appropriate tickets
        if tickets == 1:
            # Choosing the tickets
            self.api.mousePos(Cord.p_ticket1)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)   
            
            # Exit button Hit in case ticket is already chosen
            self.api.mousePos(Cord.p_tMenuExit)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)            
                   
        elif tokens == 5:
            
            # Choosing the token
            self.api.mousePos(Cord.p_ticket5)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)   
            
            # Exit button Hit in case token is already chosen
            self.api.mousePos(Cord.p_tMenuExit)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)            
            
        else:
            raise ValueError('Undefined Token Choice')   


        # Hit Play
        self.api.mousePos(Cord.p_start)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)        
        
        # Choose Fight
        self.api.mousePos(Cord.p_firstFight)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)          
        
        # Team accept
        self.api.mousePos(Cord.u_teamAccept)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)
        
        # Move Mouse out of way
        self.api.mousePos(Cord.u_outOfWay)
    
    
    
    def detectPVPVictory(self):
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
        
    def eventHandle(self):
        '''
        this will look for familiar detection and victory detection.
        it will handle both those events. upon victory, it will put 
        us back to the home menu. 
        '''
        while not self.detectGauntletVictory():
            pass
        
        print('Victory!') 
              
        # Exiting Tokens
        time.sleep(.4)
        self.api.mousePos(Cord.q_victExit) # for quests, but works here too
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(3)            
        
        # Returning to the main menu
        self.api.mousePos(Cord.g_menuExit)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)
        
        # Put mouse out of the way
        self.api.mousePos(Cord.u_outOfWay)
    
    def setResources(self,amount):
        self.resources = amount
    
    def main(self,tokens):
        '''
        Keeps running the specified raid till resources
        are finished.
        '''
        while self.resources-tokens >= 0:
            self._chooseTokens(tokens)
            self.eventHandle()
            time.sleep(2)
            self.resources -= tokens
        print('Gauntlet/Trial Farm Finished!')        

if __name__ == '__main__':
    d = GauntletCrawler()
    d.main(1) #Tokens   