with open('data/csgo_stats.txt') as f:
    data = f.read().split('\n')

def parseScore(s):
    result = s.split(':')
    return int(result[0].strip()), int(result[1].strip())  

class Game:
    def __init__(self, name, gameMap, score, position, playedTime, personalData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playerName = name
        self.gameMap = gameMap
        self.score = score
        self.position = position
        self.result = self.jugdeResult()
        self.playedTime = playedTime
        self.personalData = personalData

    def jugdeResult(self):
        left, right = self.score
        left = int(left)
        right = int(right)
        if left == right:            
            return "D"    
        if(self.position):
            if left > right:            
                return "W"
            elif left < right:             
                return "L"
        else:
            if left > right:            
                return "L"
            elif left < right:             
                return "W"   
    
    def psg(self):
        print( self.personalData)
        if self.personalData[-2] == '':
            return 0
        return float(self.personalData[-2].strip("%"))

    def ping(self):
        return int(self.personalData[0])    
    def kills(self):
        return int(self.personalData[1])
    def assists(self):
        return int(self.personalData[2])
    def deaths(self):
        return int(self.personalData[3])
    def mvps(self):
        print(self.personalData[-3])
        if self.personalData[-3] != '' and self.personalData[-3][1:] != '':
            return int(self.personalData[-3][1:])         
        return 0
    def points(self):
        return int(self.personalData[-1])

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}".format(self.playerName, self.gameMap, self.score, self.position, self. playedTime, self.result)

result = dict(W=0,D=0,L=0)

games = list()

gameMap = name = None
result = None
left = right = score = playedTime = personalData = None
position = None

i = 0
while i < len(data):
    entry = [ item for item in data[i].split(' ') if item != ''] 
    if len(entry) == 0:
        i = i + 1
        continue
    if entry[0] == 'Turniejowy':
        if (score != None and gameMap != None and position != None):
            games.append(Game(name, gameMap, score, position, playedTime, personalData))
            gameMap = name = score = position = playedTime = personalData = None
        gameMap = entry[1].strip()
    if entry[0] == "Czas" and entry[1] == "trwania":
        playedTime = entry[-1]
    if len(entry) == 3 and entry[1] == ":":
        score = entry[0], entry[2]        
    if entry[0] == 'bifi':
        name = "bifi"
    if name and not personalData and "\t" in entry[0]:
        personalData = ''.join(entry).split('\t')        
        print('personalData',personalData)

    if name != None and score != None and position == None:
        position = False
    if name != None and score == None and position == None:
        position = True
    i = i + 1

games.append(Game(name, gameMap, score, position, playedTime, personalData))
won = drawn = lost = totalMinutes = totalseconds = 0
psg = ping = kills = assist = death = points = mvp = 0 
gamesPerMap = dict()
for g in games:
    print (g)
    gamesPerMap.setdefault(g.gameMap, [0,0,0])
    if g.result == 'W':
         won = won + 1
         gamesPerMap[g.gameMap][0] += 1 
    if g.result == 'D':
         drawn = drawn + 1
         gamesPerMap[g.gameMap][1] += 1
    if g.result == 'L':
         lost = lost + 1
         gamesPerMap[g.gameMap][2] += 1
    playedMinutes = g.playedTime.split(":")[0]
    playedSeconds = g.playedTime.split(":")[1]
    totalMinutes += int(playedMinutes)
    totalseconds += int(playedSeconds)
    psg += g.psg()
    ping += g.ping()
    kills += g.kills()
    assist += g.assists()
    death += g.deaths()
    points += g.points()
    mvp += g.mvps()



print("Won: {0}, Drawn: {1}, lost: {2}".format(won , drawn, lost))
print("Minutes: {0}, Seconds: {1}".format(totalMinutes , totalseconds))
hours = int((totalMinutes * 60 + totalseconds)/3600)
minutes = (totalMinutes * 60 + totalseconds)%3600/60
print("Hours: {0}, Minutes: {1}".format(hours , minutes))

for m in gamesPerMap:
    print("Map: {0}, stats: {1}".format(m , gamesPerMap[m]))

avgPsg = round(psg/len(games),2)
avgPing = round(ping/len(games),2)
avgKills = round(kills/len(games),2)
avgAssist = round(assist/len(games),2)
avgDeath = round(death/len(games),2)
avgMvp = round(mvp/len(games),2)
avgPoints = round(points/len(games),2)

print("avgPsg: {0}".format(avgPsg))    
print("avgPing: {0}".format(avgPing))    
print("avgKills: {0}".format(avgKills))    
print("avgAssist: {0}".format(avgAssist))    
print("avgDeath: {0}".format(avgDeath))    
print("avgMvp: {0}".format(avgMvp))    
print("avgPoints: {0}".format(avgPoints))    