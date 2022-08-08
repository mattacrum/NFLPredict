from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv

'''
Web Scrape turnover margins
'''
def getTurnoverMargins():
    turnover_margin_url = 'https://www.teamrankings.com/nfl/stat/turnover-margin-per-game'
    turnover_margin_data = urlopen(turnover_margin_url)
    turnover_margin_html = turnover_margin_data.read()
    turnover_margin_data.close()

    # String of entire page
    page_soup = soup(turnover_margin_html, 'html.parser')

    # Create lists of teams and turnover margins
    teams = page_soup.findAll('td', {'class' : 'text-left nowrap'})
    turnover_margins = page_soup.findAll('td', {'class' : 'text-right'})

    tm_text = []
    teams_text = []
    for tm in turnover_margins:
        tm_text.append(float(tm.text))

    # Change abbreviated team names
    for team in teams:
        temp = team.text
        if "LA" in temp:
            if "Rams" in temp:
                temp = "Los Angeles Rams"
            if "Chargers" in temp:
                temp = "Los Angeles Chargers"
        if "NY" in temp:
            if "Giants" in temp:
                temp = "New York Giants"
            if "Jets" in temp:
                temp = "New York Jets"
        teams_text.append(temp)

    # Find average turnover margin (scewed towards last few games)
    avg_tm = []
    j = 1
    for i in range(len(tm_text)):
        if(i > 0):
            if (j % 6) == 0:
                temp = (tm_text[i-3] + tm_text[i-4] + tm_text[i-5]) / 3
                avg_tm.append(temp)
        j += 1
    # Create dictionary with team name & turnover margin
    avg_tm_dict = {teams_text[i]: avg_tm[i] for i in range(len(teams_text))}
    #print(avg_tm_dict)
    return avg_tm_dict

'''
Web Srape point differential over entire season
'''
def getTotalPointDifferential():
    point_differential_url = 'https://www.pro-football-reference.com/years/2020/index.htm'
    point_differential_data = urlopen(point_differential_url)
    point_differential_html = point_differential_data.read()
    point_differential_data.close()

    page_soup = soup(point_differential_html, 'html.parser')

    # Create lists of point differential & team names
    point_differentials = page_soup.findAll('td', {'data-stat' : 'points_diff'})
    team_names = page_soup.findAll('th', {'data-stat' : 'team', 'class' : 'left '})

    pd_text = []
    tn_text = []
    _teams_text = []
    for pd in point_differentials:
        pd_text.append(float(pd.text))

    for team in team_names:
        tn_text.append(team.text)

    avg_tm_dict = {tn_text[i]: avg_tm[i] for i in range(len(tn_text))}

    # Create dictionary with team name & point differential
    pd_dict = {tn_text[i]: pd_text[i] for i in range(len(tn_text))}

'''
Web Srape average point differential per game
'''
def getAvgPointDifferential():
    avg_point_differential_url = 'https://www.teamrankings.com/nfl/stat/average-scoring-margin'
    avg_point_differential_data = urlopen(avg_point_differential_url)
    avg_point_differential_html = avg_point_differential_data.read()
    avg_point_differential_data.close()

    page_soup = soup(avg_point_differential_html, 'html.parser')

    # Create lists of teams and avg_point differential
    teams = page_soup.findAll('td', {'class' : 'text-left nowrap'})
    avg_point_differentials = page_soup.findAll('td', {'class' : 'text-right'})

    pd_text = []
    teams_text = []
    for pd in avg_point_differentials:
        pd_text.append(float(pd.text))

    # Change abbreviated team names
    for team in teams:
        temp = team.text
        if "LA" in temp:
            if "Rams" in temp:
                temp = "Los Angeles Rams"
            if "Chargers" in temp:
                temp = "Los Angeles Chargers"
        if "NY" in temp:
            if "Giants" in temp:
                temp = "New York Giants"
            if "Jets" in temp:
                temp = "New York Jets"
        teams_text.append(temp)

    # Find average point differential (scewed towards last few games)
    avg_pd = []

    j = 1
    for i in range(len(pd_text)):
        if(i > 0):
            if (j % 6) == 0:
            #    print(pd_text[i-3], pd_text[i-4])
                temp = (pd_text[i-3] + pd_text[i-4] + pd_text[i-5]) / 3
                avg_pd.append(temp)
        j+=1

    # Create dictionary with team name & avg_point differential
    pd_dict = {teams_text[i]: avg_pd[i] for i in range(len(teams_text))}

    return pd_dict

'''
Web Srape drive success rate and time of possession per drive

****
Find new URL
****
'''
def getAvgTimeOfPossession():
    avg_TOP_url = 'https://www.teamrankings.com/nfl/stat/average-time-of-possession-net-of-ot'
    avg_TOP_data = urlopen(avg_TOP_url)
    avg_TOP_html = avg_TOP_data.read()
    avg_TOP_data.close()

    page_soup = soup(avg_TOP_html, 'html.parser')

    # Create lists of teams and average time of possession
    teams = page_soup.findAll('td', {'class' : 'text-left nowrap'})
    avg_TOP = page_soup.findAll('td', {'class' : 'text-right'})

    TOP_text = []
    teams_text = []
    i = 0
    for top in avg_TOP:
        if i % 6 == 0:
            TOP_text.append(top.text)
        i += 1
    print(TOP_text)
    # Change abbreviated team names
    for team in teams:
        temp = team.text
        if "LA" in temp:
            if "Rams" in temp:
                temp = "Los Angeles Rams"
            if "Chargers" in temp:
                temp = "Los Angeles Chargers"
        if "NY" in temp:
            if "Giants" in temp:
                temp = "New York Giants"
            if "Jets" in temp:
                temp = "New York Jets"
        teams_text.append(temp)

    # Convert TOP to seconds
    temp = []
    for time in TOP_text:
        temp.append(float(time[0:2]) * 60 + float(time[3:5]))

    # Find average Time of Possession (scewed towards last few games)
    TOP_text = temp
    avg_top = []

    j = 1
    for i in range(len(TOP_text)):

        if(i > 0):
            if (j % 6) == 0:
                temp = (TOP_text[i-4] + TOP_text[i-5]) / 2
                avg_top.append(temp)
        j+=1

    # Create dictionary with team name & avg_point differential
    top_dict = {teams_text[i]: TOP_text[i] for i in range(len(teams_text))}

    return top_dict

'''
Web Scrape Points per Game

'''
def getPointsPerGame():
    # Offensive stats from espn
    table_url = 'https://www.espn.com/nfl/stats/team'
    table_data = urlopen(table_url)
    table_html = table_data.read()
    table_data.close()

    page_soup = soup(table_html, 'html.parser')

    # List of tables containing team names and stats
    tables = page_soup.findAll('tbody', {})

    # Table of team names
    teams_html = tables[0]
    # Create list of team names
    teams = []
    for team in teams_html:
        teams.append(team.text.splitlines())

    # Table of offensive stats
    stats_html = tables[1]
    stats_html = stats_html.findAll('td', {})
    ppg = []

    i = 1
    for stat in stats_html:
        if i % 9 == 0:
            ppg.append(float(stat.text))
        i += 1


    # Create point per game Dictionaty
    ppg_dict = {teams[i][0]: float(ppg[i]) for i in range(len(teams))}

    # Change Washington
    key = "Washington"
    ppg_dict["Washington Football Team"] = ppg_dict[key]
    del ppg_dict[key]

    return ppg_dict

def getOppPointsPerGame():
    # Deffensive stats from espn
    table_url = 'https://www.espn.com/nfl/stats/team/_/view/defense'
    table_data = urlopen(table_url)
    table_html = table_data.read()
    table_data.close()

    page_soup = soup(table_html, 'html.parser')

    # List of tables containing team names and stats
    tables = page_soup.findAll('tbody', {})

    # Table of team names
    teams_html = tables[0]
    # Create list of team names
    teams = []
    for team in teams_html:
        teams.append(team.text.splitlines())

    # Table of offensive stats
    stats_html = tables[1]
    stats_html = stats_html.findAll('td', {})
    oppg = []

    i = 1
    for stat in stats_html:
        if i % 9 == 0:
            oppg.append(float(stat.text))
        i += 1

    # Create Opponent Points per Game Dictionaty
    oppg_dict = {teams[i][0]: float(oppg[i]) for i in range(len(teams))}

    # Change Washington
    key = "Washington"
    oppg_dict["Washington Football Team"] = oppg_dict[key]
    del oppg_dict[key]

    return oppg_dict

'''
Defense
*Web Scrape Turnovers per drive and Punts per drive
'''

'''
Web Scrape Opponent Yards per Game
* Probably won't use
'''
def getOppYPG():
    opp_ypg_url = 'https://www.teamrankings.com/nfl/stat/opponent-yards-per-game'
    opp_ypg_data = urlopen(opp_ypg_url)
    opp_ypg_html = opp_ypg_data.read()
    opp_ypg_data.close()

    page_soup = soup(opp_ypg_html, 'html.parser')

    # List of all opponents' yards per game
    opp_ypg = page_soup.findAll('td', {'class' : 'text-right'})
    # List of teams
    temp = page_soup.findAll('td', {'class' : 'text-left nowrap'})
    _teams = []
    for line in temp:
        _teams.append(line.text)

    # Create list of Opponents yards per game in 2020
    opp_ypg_TT = []
    i=0
    for line in opp_ypg:
        if i % 6 == 0:
            opp_ypg_TT.append(float(line.text))
        i+=1
    # Change abbreviated team names
    teams_text = []
    for team in _teams:
        temp = team
        if "LA" in temp:
            if "Rams" in temp:
                temp = "Los Angeles Rams"
            if "Chargers" in temp:
                temp = "Los Angeles Chargers"
        if "NY" in temp:
            if "Giants" in temp:
                temp = "New York Giants"
            if "Jets" in temp:
                temp = "New York Jets"
        teams_text.append(temp)
    # Create dictionary for opponents yards per game
    opp_ypg_dict = {teams_text[i]: opp_ypg_TT[i] for i in range(len(teams_text))}
    #print(opp_ypg_dict)

    return opp_ypg_dict

def changeAbbrNames(score):

    # Change abbreviated team names
    key = "GB"
    score["Green Bay Packers"] = score[key]
    del score[key]

    key = "TEN"
    score["Tennessee Titans"] = score[key]
    del score[key]

    key = "SEA"
    score["Seattle Seahawks"] = score[key]
    del score[key]

    key = "KC"
    score["Kansas City Chiefs"] = score[key]
    del score[key]

    key = "NO"
    score["New Orleans Saints"] = score[key]
    del score[key]

    key = "LV"
    score["Las Vegas Raiders"] = score[key]
    del score[key]

    key = "PIT"
    score["Pittsburgh Steelers"] = score[key]
    del score[key]

    key = "DAL"
    score["Dallas Cowboys"] = score[key]
    del score[key]

    key = "PHI"
    score["Philadelphia Eagles"] = score[key]
    del score[key]

    key = "NYJ"
    score["New York Jets"] = score[key]
    del score[key]

    key = "NYG"
    score["New York Giants"] = score[key]
    del score[key]

    key = "BAL"
    score["Baltimore Ravens"] = score[key]
    del score[key]

    key = "LAR"
    score["Los Angeles Rams"] = score[key]
    del score[key]

    key = "LAC"
    score["Los Angeles Chargers"] = score[key]
    del score[key]

    key = "BUF"
    score["Buffalo Bills"] = score[key]
    del score[key]

    key = "CLE"
    score["Cleveland Browns"] = score[key]
    del score[key]

    key = "TB"
    score["Tampa Bay Buccaneers"] = score[key]
    del score[key]

    key = "SF"
    score["San Francisco 49ers"] = score[key]
    del score[key]

    key = "ARI"
    score["Arizona Cardinals"] = score[key]
    del score[key]

    key = "ATL"
    score["Atlanta Falcons"] = score[key]
    del score[key]

    key = "CAR"
    score["Carolina Panthers"] = score[key]
    del score[key]

    key = "DET"
    score["Detroit Lions"] = score[key]
    del score[key]

    key = "IND"
    score["Indianapolis Colts"] = score[key]
    del score[key]

    key = "CIN"
    score["Cincinnati Bengals"] = score[key]
    del score[key]

    key = "NE"
    score["New England Patriots"] = score[key]
    del score[key]

    key = "WAS"
    score["Washington Football Team"] = score[key]
    del score[key]

    key = "DEN"
    score["Denver Broncos"] = score[key]
    del score[key]

    key = "JAX"
    score["Jacksonville Jaguars"] = score[key]
    del score[key]

    key = "CHI"
    score["Chicago Bears"] = score[key]
    del score[key]

    key = "MIN"
    score["Minnesota Vikings"] = score[key]
    del score[key]

    key = "HOU"
    score["Houston Texans"] = score[key]
    del score[key]

    key = "MIA"
    score["Miami Dolphins"] = score[key]
    del score[key]

    return score

'''
Print score sorted
'''
def printScore(score):
    print("Power Rankings:")
    Rankings = sorted(score.items(), key=lambda x: x[1], reverse=True)

    for team, score in Rankings:
        print(team, ": ", score)
    print("\n\n")

'''
Scale average turnover margins and point differentials

Formula to scale numbers to certain range:
Y = n * (X - Xmin) / Xrange
Y - adjusted variable
X - original variable
Xrange = Xmax - Xmin
n = upper limit of rescaled value
'''
def scaleTMandPD(avg_tm, pd_text):
    temp_tm= []
    teams_tm = []
    temp_pd = []
    teams_pd = []

    for key in avg_tm:
        temp_tm.append(float(avg_tm[key]))
        teams_tm.append(key)
    min_avg_tm = min(temp_tm)
    max_avg_tm = max(temp_tm)
    range_avg_tm = max_avg_tm - min_avg_tm

    for key in pd_text:
        temp_pd.append(float(pd_text[key]))
        teams_pd.append(key)
    min_pd = min(temp_pd)
    max_pd = max(temp_pd)
    range_pd = max_pd - min_pd

    tm_scaled = []
    for tm in temp_tm:
        temp = (tm - min_avg_tm)/range_avg_tm * 100
        tm_scaled.append(temp)

    avg_tm_scaled_dict = {teams_tm[i]: tm_scaled[i] for i in range(len(teams_tm))}
    #print(sorted(avg_tm_scaled_dict.items(), key=lambda x: x[1], reverse=True))
    #print("\n\n")

    pd_scaled = []
    for pd in temp_pd:
        temp = (pd - min_pd)/range_pd * 100
        pd_scaled.append(temp)

    pd_scaled_dict = {teams_pd[i]: pd_scaled[i] for i in range(len(teams_pd))}
    #print(sorted(pd_scaled_dict.items(), key=lambda x: x[1], reverse=True))
    return avg_tm_scaled_dict, pd_scaled_dict

'''
Average turnover margins and point differentials together
'''
def getAvgTMandPD(avg_tm_scaled_dict, pd_scaled_dict):
    tmpd_score = {}
    for team1 in avg_tm_scaled_dict:
        for team2 in pd_scaled_dict:
            if team1 in team2:
                tmpd_score[team2] = (avg_tm_scaled_dict[team1] + pd_scaled_dict[team2]) / 2
    return tmpd_score

'''
Web scrape coaching score
'''
def getCoachingRank():
    # Coaching score
    table_url = 'https://www.lineups.com/articles/nfl-coaching-staff-rankings-entering-2020-season/'
    table_data = urlopen(table_url)
    table_html = table_data.read()
    table_data.close()

    page_soup = soup(table_html, 'html.parser')

    # Find team names in order (rank)
    teams_html = page_soup.findAll('h3')
    teams = []
    for line in teams_html:
        teams.append(line.text)
    for item in teams:
        print(item)
        if len(item) > 0:
            if item[0] != '#':
                teams.remove(item)
        else:
            teams.remove(item)
    print(teams)
    
'''
Use dictWriter to write data to csv
'''
def writeToCSV( turnover_margins, pd_dict, PointsPerGame, OppPointsPerGame, avg_top):
    myFile = open('nfl_team_stats.csv', 'w')
    with myFile:
        myFields = ['team_name', 'turnover_margin', 'point_differential', 'PointsPerGame',
                    'Opp_PointsPerGame', 'Time_of_Possession']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writeheader()

        for team in PointsPerGame:
            writer.writerow({ 'team_name' : team, 'turnover_margin' : round(turnover_margins[team], 2), 'point_differential' : round(pd_dict[team], 2) ,
                              'PointsPerGame' : round(PointsPerGame[team], 2), 'Opp_PointsPerGame' : round(OppPointsPerGame[team], 2),
                              'Time_of_Possession' :  avg_top[team] })

'''
Change city names to team names
'''
def changeTeamNames(teams1, teams2):
    teams = {}
    for team1 in teams1:
        for team2 in teams2:
            if team1 in team2:
                teams[team2] = teams1[team1]

    return teams

def main():
    turnover_margins = getTurnoverMargins()
    avg_point_differentials = getAvgPointDifferential()
    PointsPerGame = getPointsPerGame()
    OppPointsPerGame = getOppPointsPerGame()
    OppYPG = getOppYPG()
    avg_top = getAvgTimeOfPossession()


    avg_tm_scaled_dict, pd_scaled_dict = scaleTMandPD(turnover_margins, avg_point_differentials)
    tmpd_score = getAvgTMandPD(avg_tm_scaled_dict, pd_scaled_dict)


    turnover_margins = changeTeamNames(turnover_margins, PointsPerGame)
    avg_point_differentials = changeTeamNames(avg_point_differentials, PointsPerGame)
    avg_top = changeTeamNames(avg_top, PointsPerGame)
    #tmpd_score = changeTeamNames(tmpd_score, DSRTOP_score)
    writeToCSV(turnover_margins, avg_point_differentials, PointsPerGame,
               OppPointsPerGame, avg_top)

    printScore(PointsPerGame)
    printScore(OppPointsPerGame)
    printScore(turnover_margins)
    printScore(avg_top)
    getCoachingRank()
main()

'''
Data Points:
Turnover margin
Point differential
Points per game
Opponent points per game
Time of possession
Home record vs Away record
Primetime record if primetime
record of last 3 games


'''
