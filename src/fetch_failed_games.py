import pandas as pd
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import leaguegamefinder
import os
import time
import requests
from fetch_playbyplay import get_playbyplay

season = "2018-19"

with open("data/failed_games_"+season+".txt", "r") as f:
    failed_games = [line.strip() for line in f.readlines() if line.strip()]


foul_events = []
for game in failed_games:
    try:
        pbp = get_playbyplay(game)
        if pbp.empty:
            continue  # if a game wasn't able to be fetched, skip it
        foul_event = pbp[pbp['EVENTMSGTYPE'] == 6].copy()
        foul_event['GAME_ID'] = game
        foul_events.append(foul_event)
    except Exception as e:
        print(f"Skipping game {game} due to error: {e}")

if foul_events:
    all_fouls_df = pd.concat(foul_events, ignore_index=True)  # join all dataframes in foul_events list together
    all_fouls_df.to_csv("data/foul_events_"+season+".csv", mode='a', index=False, header=False)
    print(f"Data added to fetched games")

else:
    print("No new data fetched.")

