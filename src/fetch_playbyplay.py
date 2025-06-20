import pandas as pd
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import leaguegamefinder
import os
import time
import requests

def get_games_for_season(season):
    """
    Fetch all regular season NBA game IDs for a given season.

    Parameters:
        season (str): Season in 'YYYY-YY' format (e.g. '2018-19')

    Returns:
        DataFrame: Contains one column, 'GAME_ID', listing all games that season.
    """
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season)  # query for the games in 'season'
    # the first dataframe of what is returned contains the data we want
    games_df = gamefinder.get_data_frames()[0]
    return list(games_df['GAME_ID'].drop_duplicates())

def get_playbyplay(game_id, max_retries=5, backoff=5, FAILED_LOG_PATH = "data/failed_games.txt"):
    """
    Pull play-by-play data for a single game using its game ID.
    Retry fetching the game if there was a timeout error.

    Includes:
        - EVENTNUM: Event index
        - EVENTMSGTYPE: Event type (e.g. 6 = foul)
        - PERIOD: Quarter (1 = Q1, 5 = OT1, etc.)
        - PCTIMESTRING: Time left in quarter
        - HOMEDESCRIPTION / VISITORDESCRIPTION: Text commentary
        - SCOREMARGIN: Current score margin

    Parameters:
        game_id (str): Game ID like '0021800854'
        max_retries (int): Number of times to try fetching the same Game.
        backoff (int): Exponentially increases the wait between fetching a failed Game.

    Returns:
        DataFrame: Subset of play-by-play data with key columns.
    """

    for attempt in range(max_retries):
        try:
            time.sleep(5)  # prevent triggering rate limiting
            df = playbyplayv2.PlayByPlayV2(game_id = game_id).get_data_frames()[0]
            df['SCOREMARGIN'] = df['SCOREMARGIN'].ffill()  # score margin are NaN except for when a basket is made, forward fill NaN values with latest score margin value
            df['SCOREMARGIN'] = df['SCOREMARGIN'].replace(to_replace='TIE', value=0)  # replace TIE with 0
            df['SCOREMARGIN'] = df['SCOREMARGIN'].fillna(0)  # replace NaN with 0
            df['SCOREMARGIN'] = pd.to_numeric(df['SCOREMARGIN'])  # make the column numeric
            print(f"Successfully fetched play-by-play for game {game_id}.")
            return df[['EVENTNUM', 'EVENTMSGTYPE', 'PERIOD', 'PCTIMESTRING', 'HOMEDESCRIPTION', 'VISITORDESCRIPTION', 'SCOREMARGIN']]
        
        except requests.exceptions.ReadTimeout:
            print(f"Timeout on game {game_id}, attempt {attempt + 1}/{max_retries}")
            time.sleep(backoff * (attempt + 1))  # exponential backoff
        except Exception as e:
            print(f"Other error on game {game_id}: {e}")
            return pd.DataFrame()  # return empty so concat doesn't fail

    print(f"Failed to get play-by-play for game {game_id} after {max_retries} retries.")
    with open(FAILED_LOG_PATH, "a") as f:
        f.write(f"{game_id}\n")
    return pd.DataFrame()  # return empty dataframe, avoids crashing the script

def is_foul(event):
    # eventmsgtype = 6 for fouls
    return event == 6  # returns True if event is 6

def main():
    seasons = "2023-24"
    for season in seasons:
        print('Gathering data for the {} NBA season.'.format(season))
        foul_events = []
        game_ids = get_games_for_season(season)
        for game_id in game_ids:
            try:
                pbp = get_playbyplay(game_id)
                if pbp.empty:
                    continue  # if a game wasn't able to be fetched, skip it
                foul_event = pbp[pbp['EVENTMSGTYPE'] == 6].copy()
                foul_event['GAME_ID'] = game_id
                foul_events.append(foul_event)
            except Exception as e:
                print(f"Skipping game {game_id} due to error: {e}")


        all_fouls_df = pd.concat(foul_events, ignore_index=True)  # join all dataframes in foul_events list together
        os.makedirs("data", exist_ok=True)
        out_path = f"data/foul_events_{season.replace('/', '-')}.csv"
        all_fouls_df.to_csv(out_path, index=False)
        print(f"Saved to {out_path}")

if __name__ == '__main__':
    main()

