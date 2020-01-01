import datetime

INPUTFILE = 'data/competitive.txt'
PLAYERNAME = 'bifi'
MATCHTOKEN = 'Turniejowy'
MATCHTIMETOKEN = 'Czas trwania'


def loadInputdata():
    with open(INPUTFILE) as f:
        data = f.read().split('\n')
    return data


class DataExtractor:
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
        # print(self.personalData)
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
        # print(self.personalData[-3])
        if self.personalData[-3] != '' and self.personalData[-3][1:] != '':
            return int(self.personalData[-3][1:])
        return 0

    def points(self):
        return int(self.personalData[-1])

    def rounds(self):
        left, right = self.score
        return int(left) + int(right)

    def __str__(self):
        return "{0}, {1}, {2}, {3}, {4}, {5}".format(self.playerName, self.gameMap, self.score, self.position, self. playedTime, self.result)


class DataParser:
    def __init__(self, data):
        super().__init__()
        self.data = data

    def parse(self):
        games = list()
        gameMap = None
        name = None
        score = None
        playedTime = None
        personalData = None
        position = None

        i = 0
        while i < len(data):
            entry = [item for item in self.data[i].split(' ') if item != '']
            if len(entry) == 0:
                i = i + 1
                continue
            if entry[0] == MATCHTOKEN:
                if (score != None and gameMap != None and position != None):
                    games.append(DataExtractor(name, gameMap, score,
                                               position, playedTime, personalData))
                    gameMap = name = score = position = playedTime = personalData = None
                gameMap = entry[1].strip()
            if len(entry) > 1 and ' '.join([entry[0], entry[1]]) == MATCHTIMETOKEN:
                playedTime = entry[-1]
            if len(entry) == 3 and entry[1] == ":":
                score = entry[0], entry[2]
            if entry[0] == PLAYERNAME:
                name = PLAYERNAME
            if name and not personalData and "\t" in entry[0]:
                personalData = ''.join(entry).split('\t')
            if name != None and score != None and position == None:
                position = False
            if name != None and score == None and position == None:
                position = True
            i = i + 1

        games.append(DataExtractor(name, gameMap, score,
                                   position, playedTime, personalData))
        return games


class GameStatistics:
    def __init__(self, games):
        super().__init__()
        self.games = games
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.totalMinutes = 0
        self.totalseconds = 0
        self.psg = 0
        self.ping = 0
        self.ping_zero = 0
        self.kills = 0
        self.assist = 0
        self.death = 0
        self.points = 0
        self.mvp = 0
        self.rounds = 0
        self.gamesPerMap = dict()

    def calculate(self):
        for g in self.games:
            # print(g)
            self.gamesPerMap.setdefault(g.gameMap, [0, 0, 0])
            if g.result == 'W':
                self.won += 1
                self.gamesPerMap[g.gameMap][0] += 1
            if g.result == 'D':
                self.drawn += 1
                self.gamesPerMap[g.gameMap][1] += 1
            if g.result == 'L':
                self.lost += 1
                self.gamesPerMap[g.gameMap][2] += 1
            playedMinutes = g.playedTime.split(":")[0]
            playedSeconds = g.playedTime.split(":")[1]
            self.totalMinutes += int(playedMinutes)
            self.totalseconds += int(playedSeconds)
            self.psg += g.psg()
            self.ping += g.ping()
            if(g.ping() == 0 ):                
                self.ping_zero += 1
            self.kills += g.kills()
            self.assist += g.assists()
            self.death += g.deaths()
            self.points += g.points()
            self.mvp += g.mvps()
            self.rounds += g.rounds()


class DataFormatter:
    def __init__(self, gameStatistics):
        super().__init__()
        self.gameStatistics = gameStatistics

    def show(self):
        print("Won: {0}, Drawn: {1}, lost: {2}".format(
            self.gameStatistics.won, self.gameStatistics.drawn, self.gameStatistics.lost))
        print("Minutes: {0}, Seconds: {1}".format(
            self.gameStatistics.totalMinutes, self.gameStatistics.totalseconds))
        hours = int((self.gameStatistics.totalMinutes * 60 +
                     self.gameStatistics.totalseconds)/3600)
        minutes = (self.gameStatistics.totalMinutes * 60 +
                   self.gameStatistics.totalseconds) % 3600/60
        print("Hours: {0}, Minutes: {1}".format(hours, minutes))

        for m in self.gameStatistics.gamesPerMap:
            print("Map: {0}, stats: {1}".format(
                m, self.gameStatistics.gamesPerMap[m]))

        totalKills = self.gameStatistics.kills
        totalDeaths = self.gameStatistics.death
        totalAssist = self.gameStatistics.assist
        totalMPVs = self.gameStatistics.mvp
        kdRatio = round(totalKills/totalDeaths, 2)
        roundsPlayed = self.gameStatistics.rounds

        avgPsg = round(self.gameStatistics.psg/len(games), 2)
        avgPing = round(self.gameStatistics.ping/len(games), 2)
        avgKills = round(self.gameStatistics.kills/len(games), 2)
        avgAssist = round(self.gameStatistics.assist/len(games), 2)
        avgDeath = round(self.gameStatistics.death/len(games), 2)
        avgMvp = round(self.gameStatistics.mvp/len(games), 2)
        avgPoints = round(self.gameStatistics.points/len(games), 2)

        print("avgPsg: {0}".format(avgPsg))
        print("avgPing: {0}".format(avgPing))
        print("avgKills: {0}".format(avgKills))
        print("avgAssist: {0}".format(avgAssist))
        print("avgDeath: {0}".format(avgDeath))
        print("avgMvp: {0}".format(avgMvp))
        print("avgPoints: {0}".format(avgPoints))

        print("totalKills: {0}".format(totalKills))
        print("totalDeaths: {0}".format(totalDeaths))
        print("totalAssist: {0}".format(totalAssist))
        print("totalMPVs: {0}".format(totalMPVs))
        print("kdRatio: {0}".format(kdRatio))
        print("roundsPlayed: {0}".format(roundsPlayed))
        print("kicked/left: {0}".format(self.gameStatistics.ping_zero))

        f = open('competitive_statistics.txt', 'w')
        output = "𝐏𝐥𝐚𝐲𝐞𝐫: {0}\n".format(PLAYERNAME)        
        f.write(output)
        output = "\n𝐆𝐚𝐦𝐞 𝐦𝐨𝐝𝐞: competitive 5v5\n"
        f.write(output)
        allGames = sum([self.gameStatistics.won, self.gameStatistics.drawn, self.gameStatistics.lost])
        output = "\n𝐆𝐚𝐦𝐞𝐬 𝐩𝐥𝐚𝐲𝐞𝐝: {0}, 𝐖𝐨𝐧: {1}, 𝐃𝐫𝐚𝐰𝐧: {2}, 𝐋𝐨𝐬𝐭: {3}\n".format(allGames, self.gameStatistics.won, self.gameStatistics.drawn, self.gameStatistics.lost)
        f.write(output)
        output = "\n𝐆𝐚𝐦𝐞𝐬 𝐝𝐢𝐬𝐭𝐫𝐢𝐛𝐮𝐭𝐢𝐨𝐧 𝐩𝐞𝐫 𝐦𝐚𝐩:\n"
        f.write(output)

        for m in sorted(self.gameStatistics.gamesPerMap):
            output = "▪️ {0}: {1} ({2}/{3}/{4})\n".format(m, sum(self.gameStatistics.gamesPerMap[m]), self.gameStatistics.gamesPerMap[m][0], self.gameStatistics.gamesPerMap[m][1], self.gameStatistics.gamesPerMap[m][2])
            f.write(output)
        output = "\n𝐈𝐧-𝐠𝐚𝐦𝐞 𝐭𝐨𝐭𝐚𝐥 𝐩𝐞𝐫𝐟𝐨𝐫𝐦𝐚𝐧𝐜𝐞:\n"
        f.write(output)
        output = "▪️ Total kills: {0}\n".format(totalKills)
        f.write(output)
        output = "▪️ Total deaths: {0}\n".format(totalDeaths)
        f.write(output)
        output = "▪️ Total assists: {0}\n".format(totalAssist)
        f.write(output)
        output = "▪️ Total MVPs: {0}\n".format(totalMPVs)
        f.write(output)
        output = "▪️ K/D ratio: {0}\n".format(kdRatio)
        f.write(output)
        output = "▪️ Rounds played: {0}\n".format(roundsPlayed)
        f.write(output)
        output = "\n𝐈𝐧-𝐠𝐚𝐦𝐞 𝐚𝐯𝐞𝐫𝐚𝐠𝐞 𝐩𝐞𝐫𝐟𝐨𝐫𝐦𝐚𝐧𝐜𝐞:\n"
        f.write(output)
        output = "▪️ Avg. Headshot: {0}%\n".format(avgPsg)
        f.write(output)
        output = "▪️ Avg. Ping: {0} ms\n".format(avgPing)
        f.write(output)
        output = "▪️ Avg. Kills: {0} 😃\n".format(avgKills)
        f.write(output)
        output = "▪️ Avg. Assists: {0} 😉\n".format(avgAssist)
        f.write(output)
        output = "▪️ Avg. Deaths: {0} 😡\n".format(avgDeath)
        f.write(output)
        output = "▪️ Avg. MVPs: {0} ⭐️\n".format(avgMvp)
        f.write(output)
        output = "▪️ Avg. Points: {0}\n".format(avgPoints)
        f.write(output)
        output = "\n𝐎𝐭𝐡𝐞𝐫:\n"
        f.write(output)
        output = "▪️ Kicked out or left: {0} times\n".format(self.gameStatistics.ping_zero)
        f.write(output)
        output = "\n𝐑𝐞𝐚𝐥 𝐓𝐢𝐦𝐞 𝐏𝐥𝐚𝐲𝐞𝐝:\n"
        f.write(output)
        output = "▪️ Competitive: {0} hours {1} minutes\n".format(hours, int(minutes))
        f.write(output)
      
        output = "\n𝘓𝘢𝘴𝘵 𝘶𝘱𝘥𝘢𝘵𝘦𝘥: {0}".format(datetime.datetime.now())
        f.write(output)

        f.close()
   

data = loadInputdata()
games = DataParser(data).parse()
statistics = GameStatistics(games)
statistics.calculate()
DataFormatter(statistics).show()

# CSGO:
# https://github.com/80220/csgo

# INSURGENCY:
# <TBD>