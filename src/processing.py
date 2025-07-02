import pandas as pd
import os

season = "2024-25"
season_type = "playoff"  # change depending on season type, either regular season or playoff
data_path = "data/foul_events_"+season+"_"+season_type+".csv"
foul_events = pd.read_csv(data_path)
foul_events = foul_events[["GAME_ID", "PERIOD", "PCTIMESTRING", "HOMEDESCRIPTION", "VISITORDESCRIPTION", "SCOREMARGIN", "PLAYER1_ID", "PLAYER2_ID"]]
foul_events = foul_events.astype({'PCTIMESTRING':'string', 'HOMEDESCRIPTION':'string', 'VISITORDESCRIPTION':'string'})
foul_events['HOMEDESCRIPTION'] = foul_events['HOMEDESCRIPTION'].fillna('')
foul_events['VISITORDESCRIPTION'] = foul_events['VISITORDESCRIPTION'].fillna('')

def get_sec(time_str):
    "Get seconds from time."
    minutes, seconds = time_str.split(':')
    return (int(minutes)*60) + int(seconds)

foul_events['PCTIMESTRING'] = foul_events['PCTIMESTRING'].apply(get_sec)

def clean_foul(foul):
    foul = foul.lower()
    known_fouls = [
        'p.foul',
        's.foul',
        'off.foul',
        'l.b.foul',
        'flagrant.foul.type1',
        'flagrant.foul.type2',
        'away.from.play.foul',
        'offensive charge foul',
        't.foul',
        'personal take foul',
        'transition take foul',
        'hanging.tech.foul',
        'non-unsportsmanlike tech foul - flopping',
        'non-unsportsmanlike tech foul - bench',
        'too many players tech foul',
        'punch.foul',
        'personal block foul',
        'shooting block foul',
        'in.foul'
    ]
    
    for known in known_fouls:
        if known in foul:
            return known
    if 'no foul' in foul:
        return None
    if 'foul' in foul:
        print(foul)  # if none of the fouls matched, but foul is present in the text, print it so i can add to the list
        return 'foul'  # if none of the fouls matched, but foul is present in the text, preserve it
        
foul_events['HOMEDESCRIPTION'] = foul_events['HOMEDESCRIPTION'].apply(clean_foul)
foul_events['VISITORDESCRIPTION'] = foul_events['VISITORDESCRIPTION'].apply(clean_foul)

foul_events.to_csv(data_path, index=False)
print(f"Saved to {data_path}")