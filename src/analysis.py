import pandas as pd
import os

season = '2024-25'
fouls = pd.read_csv(f'data/clean_foul_events_{season}.csv')

overtime_fouls = fouls[fouls['PERIOD'] > 4].copy()  # fouls committed in overtime -> how does it compare to fouls in regular time?

# get all fouls committed in games that go into overtime (so regular time + overtime)
# the following can be used to answer if fewer fouls are called as the game gets longer
game_ids = fouls.query("PERIOD > 4")['GAME_ID'].copy()
game_ids = game_ids.drop_duplicates()
game_ids_l = game_ids.values.tolist()
overtime_games = fouls[fouls['GAME_ID'].isin(game_ids_l)]

no_overtime = fouls[fouls['PERIOD'] <= 4].copy()  # all fouls committed in 1-4 quarter

# fouls committed in the last two mins of the 4th quarter
last_two_mins = no_overtime[(no_overtime['PERIOD'] == 4) & (no_overtime['PCTIMESTRING']<=120)]
last_two_mins = last_two_mins.copy()
last_two_mins['IS_CLOSE_GAME'] = last_two_mins['SCOREMARGIN'].abs() <= 5

# fouls committed not in the last two mins of the game 
rest = no_overtime[~((no_overtime['PERIOD'] == 4) & (no_overtime['PCTIMESTRING']<=120))]

n_games = no_overtime['GAME_ID'].nunique()  # number of unique games

fouls_last2 = len(last_two_mins)  # number of fouls in last two mins of 4th quarter
fouls_rest = len(rest)

# total time across all games
total_time_last2 = n_games * 2  # 2 minutes per game
total_time_rest = n_games * (48 - 2)  # 46 minutes per game

# foul rates
rate_last2 = fouls_last2 / total_time_last2
rate_rest = fouls_rest / total_time_rest

print("Foul rate (last 2 mins):", rate_last2, "fouls per minute")
print("Foul rate (rest of game):", rate_rest, "fouls per minute")
