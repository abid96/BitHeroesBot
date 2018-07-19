'''
Will do both gauntlet/trial and GvG
'''
from gauntlet import GauntletCrawler
from gvg import GvGCrawler
from dungeon import DungeonCrawler
from raid import RaidCrawler


tokens = 10
gvgTokens = 0#10
energy = 179
shards = 4

#-------------
g = GauntletCrawler()
g.setResources(tokens)
g.main(5) #Number of tokens

v = GvGCrawler()
v.setResources(gvgTokens) 
v.main(5) # number of tokens

d = DungeonCrawler()
d.setResources(energy)
d.main(4,3,3) #Zone,dungeon,difficulty

r = RaidCrawler()
r.setResources(shards)
r.main(1,3) #Raid,difficulty
