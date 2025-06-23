import pandas as pd
import os

season = "2018-19"
data_path = "data/foul_events_"+season+".csv"
foul_events = pd.read_csv(data_path)
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
        'personal take foul'
    ]
    
    for known in known_fouls:
        if known in foul:
            return known
    if 'foul' in foul:
        return 'foul'  # if none of the fouls matched, but foul is present in the text, preserve it#
        
foul_events['HOMEDESCRIPTION'] = foul_events['HOMEDESCRIPTION'].apply(clean_foul)
foul_events['VISITORDESCRIPTION'] = foul_events['VISITORDESCRIPTION'].apply(clean_foul)

out_path = f"data/clean_foul_events_{season}.csv"
foul_events.to_csv(out_path, index=False)
print(f"Saved to {out_path}")