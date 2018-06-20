tag = raw_input("Enter Tag:")
slug = raw_input("Enter Slug:")

import requests
import pandas as pd
import datetime

response = requests.get("https://api.smash.gg/tournament/%s?expand[]=entrants" % slug)
data = response.json()['entities']['player']
for i in range(len(data)):
    if data[i]["gamerTag"].lower() == tag.lower():
        playerID = data[i]["id"]
response = requests.get("https://api.smash.gg/player/%s?expand[]=phase_groups" % playerID)
tournaments = response.json()['entities']['attendee']

bugged_tourneys = []
good_tourneys = []

for i in range(len(tournaments)):
    entrant_list = tournaments[i]['entrants']
    tourneyname = tournaments[i]['events'][0]['slug'].split("/")[1]
    if 'pools' not in tournaments[i]:
        bugged_tourneys.append(tourneyname)
        
    else:
        pools_list = tournaments[i]['pools']
        event_list = tournaments[i]['events']
        entrant_list = tournaments[i]['entrants']
        for j in range(len(pools_list)):
            d = dict()
            d['tourney'] = tourneyname
            d['phaseId'] = pools_list[j]["phaseGroupId"]
            d['eventId'] = pools_list[j]["eventId"]
            for k in range(len(entrant_list)):
                if entrant_list[k]['eventId'] == pools_list[j]['eventId']:
                    d['entrantId'] = entrant_list[k]['id']
                    if len(entrant_list[k]["participantIds"]) > 1:
                        d['Dubs?'] = True
                        d['Partner'] = tournaments[i]['teamMates'][0]['gamerTag']
                    else:
                        d['Dubs?'] = False
                    break
            for k in range(len(event_list)):
                if event_list[k]['id'] == pools_list[j]['eventId']:
                    d['event'] = event_list[k]['slug'].split("/")[3]
                    break
            good_tourneys.append(d)
            
#splitting into doubles and singles
dubs = []
singles = []
for i in range(len(good_tourneys)):
    if good_tourneys[i]['Dubs?']:
        dubs.append(good_tourneys[i])
    else:
        singles.append(good_tourneys[i])
        
columns = ["Tourney","Event","Opponent","Round","Result","GamesWon","GamesLost", "Date"]
sdf = pd.DataFrame(columns=columns)
ddf = pd.DataFrame(columns=columns)

for i in range(len(singles)):
    
    tourney = singles[i]['tourney']
    event = singles[i]['event']
    
    response3 = requests.get('https://api.smash.gg/phase_group/%d?expand[]=sets' % singles[i]['phaseId'])
    
    if "sets" in response3.json()['entities']:
        sets = response3.json()['entities']['sets']
    else:
        continue
    
    response4 = requests.get('https://api.smash.gg/phase_group/%d?expand[]=entrants' % singles[i]['phaseId'])
    phase_entrants = response4.json()['entities']['entrants']
    
    for j in range(len(sets)):
        rnd = sets[j]["shortRoundText"]
        if sets[j]["entrant1Id"] == singles[i]['entrantId'] and sets[j]["entrant2Id"]:
            player_score = sets[j]["entrant1Score"]
            opp_score = sets[j]["entrant2Score"]
            #setting result
            if player_score > opp_score:
                result = "W"
            else:
                result = "L"
            #finding opp tag with opp ID
            for k in range(len(phase_entrants)):
                if sets[j]["entrant2Id"] == phase_entrants[k]['id']:
                    opp_tag = phase_entrants[k]['name'].split(" | ")[-1]
                    break
            sdf = sdf.append({'Event': event,'Date': sets[j]["completedAt"],'Opponent': opp_tag,'Round': rnd, 'Result': result, 'GamesWon': player_score,'GamesLost': opp_score, "Tourney": tourney}, ignore_index = True)
        elif sets[j]["entrant2Id"] == singles[i]['entrantId'] and sets[j]["entrant1Id"]:
            player_score = sets[j]["entrant2Score"]
            opp_score = sets[j]["entrant1Score"]
            if player_score > opp_score:
                result = "W"
            else:
                result = "L"
            for k in range(len(phase_entrants)):
                if sets[j]["entrant1Id"] == phase_entrants[k]['id']:
                    opp_tag = phase_entrants[k]['name'].split(" | ")[-1]
                    break
            sdf = sdf.append({'Event': event,'Date': sets[j]["completedAt"],'Opponent': opp_tag,'Round': rnd, 'Result': result, 'GamesWon': player_score,'GamesLost': opp_score, "Tourney": tourney}, ignore_index = True)

sdf = sdf.sort_values(by = "Date")
for i in range(len(sdf['Date'])):
    if sdf['Date'][i]:
        sdf['Date'][i] = datetime.datetime.fromtimestamp(sdf['Date'][i]).strftime('%c').split(" ")[0]

csv_name = "Results/%s_Singles_TourneyResults.csv" % (tag)
sdf.to_csv(csv_name)

print bugged_tourneys
print("Done! Check local directory for excel file.")