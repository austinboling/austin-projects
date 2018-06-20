import requests
import time

#creating directory for text files if it does not already exist
import os
if not os.path.exists('Entrants'):
    os.makedirs('Entrants')

tourney_slug = raw_input("Copy tourney name from smash.gg URL: ")
#getting tourney info so we have the tourneyID to request the stream queue
r_tourney = requests.get('https://api.smash.gg/tournament/%s' % tourney_slug)
tourney_data = r_tourney.json()
tourney_id = str(tourney_data['entities']['tournament']['id'])

#loop to keep it running indefinitely
while True:
    #getting stream queue data
    r_streams = requests.get('https://api.smash.gg/station_queue/%s' % tourney_id)
    streams_data = r_streams.json()
    
    sets = streams_data['data']['entities'].get('sets')
    entrants = streams_data['data']['entities'].get('entrants')
    
    if sets is None or entrants is None:
        #then the stream queue is empty. question marks for placeholders.
        entrant1_tag = '???'
        entrant2_tag = '???'
        round_name = '???'
    else:
        #checking if there is only one set in the stream queue, if so, API makes it dict not list
        if type(sets) == type({}):
            if sets['startedAt'] is not None and sets['completedAt'] is None:
                #then the match should be currently on stream. saving entrant ID numbers.
                entrant1_id = sets['entrant1Id']
                entrant2_id = sets['entrant2Id']
                round_name = sets['midRoundText']
        else:
            for i in range(len(sets)):
                if sets[i]['startedAt'] is not None and sets[i]['completedAt'] is None:
                    #then this match should be currently on stream. saving entrant ID numbers.
                    entrant1_id = sets[i]['entrant1Id']
                    entrant2_id = sets[i]['entrant2Id']
                    round_name = sets[i]['midRoundText']
                    break
            
        found = 0
        #if there is a currently streamed match, find entrant tags
        if entrant1_id is not None and entrant2_id is not None:
            for i in range(len(entrants)):
                if entrants[i]['id'] == entrant1_id:
                    entrant1_tag = entrants[i]['name']
                    found += 1
                elif entrants[i]['id'] == entrant2_id:
                    entrant2_tag = entrants[i]['name']
                    found += 1
                #checking to see if it has found both players' tags yet
                if found > 1:
                    break

    #writing entrant and round information to text files
    with open('Entrants/Entrant1.txt', 'w') as f:
        f.write(entrant1_tag)
    with open('Entrants/Entrant2.txt', 'w') as f:
        f.write(entrant2_tag)
    with open('Entrants/Round.txt', 'w') as f:
        f.write(round_name)
        
    #sleep cuz im not tryna mess with smash.gg
    time.sleep(15)