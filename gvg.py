'''
This is a part of a program to play the game bit heroes.
This module in particular is responsible for farming gvg
until the resources end.

v1.0

- Abid Rizvi
'''

from PIL import Image
import time
from api import Api
from Cord import Cord
import time

class GvGCrawler:
    '''
    A lot of the framework from gauntlet is used here as
    both UI's are very similar
    '''
    # NOTE: You must set the difficulty level yourself!!
    def __init__(self):
        '''
        The api module provides necessary functions for farming
        The only other global variable we need to watch are resources
        '''
        self.api = Api()
        self.api.setPads()
        self.resources = 10
        
        while not self.api.detectHomeScreen():
            self.api.reconnected()
            time.sleep(1)
    def _clickQuest(self):
        '''
        Clicks the gvg button on the main menu
        '''
        self.api.mousePos(Cord.mm_gvg)
        self.api.leftClick()
    def _chooseTokens(self,tokens):
        '''
        after clicking the gauntlet button, this method
        will then choose the tokens 
        and then click start
        '''
        # Clicking gauntlet button
        self._clickQuest()
        time.sleep(.5)
        
        # Press Token Menu
        self.api.mousePos(Cord.g_tokenMenu)
        time.sleep(.1)
        self.api.leftClick()
        time.sleep(.3) 
        
        
        # Choosing the appropriate tokens
        if tokens == 1:
            # Choosing the token
            self.api.mousePos(Cord.g_token1)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)   
            
            # Exit button Hit in case token is already chosen
            self.api.mousePos(Cord.g_tMenuExit)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)            
                   
        elif tokens == 5:
            
            # Choosing the token
            self.api.mousePos(Cord.g_token5)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)   
            
            # Exit button Hit in case token is already chosen
            self.api.mousePos(Cord.g_tMenuExit)
            time.sleep(.1)
            self.api.leftClick()
            time.sleep(.1)            
            
        else:
            raise ValueError('Undefined Token Choice')   


        # Hit Play
        self.api.mousePos(Cord.g_start)
        time.sleep(.5)
        self.api.leftClick()
        time.sleep(.5)        
        
        # Hit First fight
        self.api.mousePos(Cord.gg_firstFight)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)             
        
        # Team accept
        self.api.mousePos(Cord.gg_teamAccept)
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(.1)
        
        # Move Mouse out of way
        self.api.mousePos(Cord.u_outOfWay)
    
    
    
    def detectGauntletVictory(self):
        '''
        detects if the dungeon has been cleared. returns boolean
        '''
        a = self.api.grab(4)
        
        # This segment is needed to avoid similar looking screens.
        # This one specifically makes the item screen not pass as victory
        b = self.api.screenGrab()
        neededRGBVal = (197, 145, 0)
        gottenRGBVal = b.getpixel((410,400))
        
        c = self.api.screenGrab()
        neededRGBVal2 = (165, 211, 56)
        gottenRGBVal2  = c.getpixel((880,940))
        
        if neededRGBVal != gottenRGBVal or neededRGBVal2 != gottenRGBVal2:
            return False
        else:
            return a == 86373   
        

    def eventHandle(self):
        '''
        this will look for familiar detection and victory detection.
        it will handle both those events. upon victory, it will put 
        us back to the home menu. Note, unlike other programs, it is
        very difficult to detect the difference between defeat and victory
        but the handling is the same, so no attempt is made to distinguish
        them
        '''
        while not self.detectGauntletVictory():
            pass
        
        
        print('Victory or Defeat') 
          
        # Exiting Tokens
        time.sleep(.4)
        self.api.mousePos(Cord.gg_victoryClose) # for quests, but works here too
        time.sleep(.4)
        self.api.leftClick()
        time.sleep(3.5)     
            
        
        # Returning to the main menu
        self.api.mousePos(Cord.gg_menuExit)
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
        print('GvG Farm Finished!')        

if __name__ == '__main__':
    
    d = GvGCrawler()
    d.setResources(1)
    d.main(1)