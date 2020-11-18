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
                temp = (pd_text[i-4] + pd_text[i-5]) / 2
                avg_pd.append(temp)
        j+=1

    # Create dictionary with team name & avg_point differential
    pd_dict = {teams_text[i]: avg_pd[i] for i in range(len(teams_text))}

    return pd_dict

'''
Web Srape drive success rate and time of possession per drive
'''
def getDSRandTOP():
    table_url = 'https://www.footballoutsiders.com/stats/nfl/overall-drive-statsoff/2020'
    table_data = urlopen(table_url)
    table_html = table_data.read()
    table_data.close()

    page_soup = soup(table_html, 'html.parser')

    # List of tables containing drive stats
    table = page_soup.findAll('tbody', {})
    table = table[0]
    # List of entries in the table
    entries = table.findAll('tr',{})

    # Create lists of team names, time of possession, & drive success rate
    teams = []
    TOP = []
    DSR = []
    for entry in entries:
        team_stats = entry.text.splitlines()
        teams.append(team_stats[1])
        TOP.append(team_stats[17])
        DSR.append(float(team_stats[19]))

    # Create TOP Dictionaty
    TOP_dict = {teams[i]: TOP[i] for i in range(len(teams))}
    #Create DSR Dictionary
    DSR_dict = {teams[i]: DSR[i] for i in range(len(teams))}

    # Convert TOP to seconds
    temp = []
    for time in TOP:
        temp.append(float(time[0]) * 60 + float(time[2]) * 10 + float(time[3]))
    TOP = temp
    TOP_dict = {teams[i]: TOP[i] for i in range(len(teams))}
    return DSR, TOP, teams

'''
Web Scrape Touchdowns per drive
TD per drive - Opponet TD per drive
'''
def getTDperDrive():
    # TD per drive
    table_url = 'https://www.footballoutsiders.com/stats/nfl/overall-drive-statsoff/2020'
    table_data = urlopen(table_url)
    table_html = table_data.read()
    table_data.close()

    page_soup = soup(table_html, 'html.parser')

    # List of tables containing drive stats
    table = page_soup.findAll('tbody', {})
    table = table[1]
    # List of entries in the table
    entries = table.findAll('tr',{})

    # Create lists of team names, time of possession, & drive success rate
    teams = []
    td_drive = []

    for entry in entries:
        team_stats = entry.text.splitlines()
        teams.append(team_stats[1])
        td_drive.append(team_stats[3])

    # Create TD per drive Dictionaty
    td_drive_dict = {teams[i]: float(td_drive[i]) for i in range(len(teams))}

    return td_drive_dict

def getOppTDperDrive():
    # Opponent TD per drive
    table_url = 'https://www.footballoutsiders.com/stats/nfl/overall-drive-statsdef/2020'
    table_data = urlopen(table_url)
    table_html = table_data.read()
    table_data.close()

    page_soup = soup(table_html, 'html.parser')

    # List of tables containing drive stats
    table = page_soup.findAll('tbody', {})
    table = table[1]
    # List of entries in the table
    entries = table.findAll('tr',{})

    # Create lists of team names, time of possession, & drive success rate
    teams = []
    opp_td_drive = []

    for entry in entries:
        team_stats = entry.text.splitlines()
        teams.append(team_stats[1])
        opp_td_drive.append(team_stats[3])

    # Create Opponent TD per Drive Dictionaty
    opp_td_drive_dict = {teams[i]: float(opp_td_drive[i]) for i in range(len(teams))}

    return opp_td_drive_dict

'''
Defense
*Web Scrape Turnovers per drive and Punts per drive
'''

'''
Web Scrape Opponent Yards per Game
*Add Opponent Points per game
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

'''
Scale TOP and DSR
*possibly subtract defensive TOP and DSR

Formula to scale numbers to certain range:
Y = n * (X - Xmin) / Xrange
Y - adjusted variable
X - original variable
Xrange = Xmax - Xmin
n = upper limit of rescaled value

'''
def scaleDSRTOP(DSR,TOP, teams):
    min_TOP = min(TOP)
    max_TOP= max(TOP)
    range_TOP = max_TOP - min_TOP

    min_DSR = min(DSR)
    max_DSR = max(DSR)
    range_DSR = max_DSR - min_DSR

    TOP_scaled = []
    for time in TOP:
        temp = (time - min_TOP)/range_TOP * 100
        TOP_scaled.append(temp)

    DSR_scaled = []
    for stat in DSR:
        temp = (stat - min_DSR)/range_DSR * 100
        DSR_scaled.append(temp)

    TOP_dict_scaled = {teams[i]: TOP_scaled[i] for i in range(len(teams))}
    DSR_dict_scaled = {teams[i]: DSR[i] for i in range(len(teams))}

    '''
    DSR percentage multiplied by TOP
    '''

    dsrtop_score = {}
    for team1 in TOP_dict_scaled:
        for team2 in DSR_dict_scaled:
            if team1 in team2:
                #dsrtop_score[team2] = (TOP_dict_scaled[team1] + DSR_dict_scaled[team2]) / 2
                dsrtop_score[team2] = TOP_dict_scaled[team1] * DSR_dict_scaled[team2]
    # TODO fix this ^
    #print(sorted(dsrtop_score.items(), key=lambda x: x[1], reverse=True))
    return dsrtop_score

def changeAbbrNames(score):
    temp = {}
    #print(dsrtop_score.items())
    dsrtop_score_temp = score

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
Print power rankings based on TOP and DSR
'''
def printScore(score):
    print("Power Rankings:")
    Rankings = sorted(score.items(), key=lambda x: x[1], reverse=True)

    for team, score in Rankings:
        print(team, ": ", score)
    print("\n\n")

'''
Scale average turnover margins and point differentials
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
Use dictWriter to write data to csv
'''
def writeToCSV( avg_tm_dict, pd_dict, tmpd_score, dsrtop_score, td_drive_dict, opp_td_drive):
    myFile = open('nfl_team_stats.csv', 'w')
    with myFile:
        myFields = ['team_name', 'turnover_margin', 'point_differential', 'tm_pd_score', 'time_of_possession_DSR', 'off_td_drive', 'opp_td_drive']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writeheader()

        for team in tmpd_score:
            writer.writerow({ 'team_name' : team, 'turnover_margin' : round(avg_tm_dict[team], 2), 'point_differential' : round(pd_dict[team], 2) ,
                              'tm_pd_score' : round(tmpd_score[team], 2), 'time_of_possession_DSR' : round(dsrtop_score[team], 2),
                              'off_td_drive' :  td_drive_dict[team], 'opp_td_drive' : opp_td_drive[team] })

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
    TDperDrive = getTDperDrive()
    OppTDperDrive = getOppTDperDrive()
    OppYPG = getOppYPG()

    DSR, TOP, teams = getDSRandTOP()
    DSRTOP_score = scaleDSRTOP(DSR, TOP, teams)

    avg_tm_scaled_dict, pd_scaled_dict = scaleTMandPD(turnover_margins, avg_point_differentials)
    tmpd_score = getAvgTMandPD(avg_tm_scaled_dict, pd_scaled_dict)


    TDperDrive = changeAbbrNames(TDperDrive)
    OppTDperDrive = changeAbbrNames(OppTDperDrive)
    DSRTOP_score = changeAbbrNames(DSRTOP_score)

    turnover_margins = changeTeamNames(turnover_margins, DSRTOP_score)
    avg_point_differentials = changeTeamNames(avg_point_differentials, DSRTOP_score)
    tmpd_score = changeTeamNames(tmpd_score, DSRTOP_score)

    writeToCSV(turnover_margins, avg_point_differentials, tmpd_score, DSRTOP_score, TDperDrive, OppTDperDrive)
    #printScore(DSRTOP_score)
main()

'''
If team has better TOPDSR & lower opp_td_drive, HAMMER
If team has better td_drive and lower opp_td_drive,
'''
