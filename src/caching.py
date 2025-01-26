import csv
import os
import shutil
from src.constants import ESPN_LEAGUE_ID
from src.espn_interactions.basketball import remove_unallowed_characters


CACHE_DIRECTORY = "cached"
CACHE_TEAMS_DIRECTORY = "teams"
CACHE_SCHEDULES_DIRECTORY = "schedules"


def get_path_cache():
    return "{}/{}/".format(CACHE_DIRECTORY, ESPN_LEAGUE_ID)


def init_cache_folders():
    if not os.path.exists(CACHE_DIRECTORY):
        os.makedirs(CACHE_DIRECTORY)  # TODO: upgrade python version so i can use ", exist_ok=True" https://stackoverflow.com/questions/6004073/how-can-i-create-directories-recursively
    if not os.path.exists(get_path_cache()):
        os.makedirs(get_path_cache())
    else:
        if os.path.exists(get_path_cache()):
            shutil.rmtree(get_path_cache())
    if not os.path.exists(get_path_cache() + CACHE_TEAMS_DIRECTORY):
        os.makedirs(get_path_cache() + CACHE_TEAMS_DIRECTORY)
    if not os.path.exists(get_path_cache() + CACHE_SCHEDULES_DIRECTORY):
        os.makedirs(get_path_cache() + CACHE_SCHEDULES_DIRECTORY)


def cache_teams(teams):
    for name in teams:
        safe_name = remove_unallowed_characters(name)
        with open(
            "{}/{}/{}.csv".format(get_path_cache(), CACHE_TEAMS_DIRECTORY, safe_name), "w", newline="\n"
        ) as team_file:
            for player in teams[name]:
                writer = csv.writer(team_file)
                writer.writerow([player])


def load_teams():
    teams = {}
    for __, __, filenames in os.walk("./{}/{}/".format(get_path_cache(), CACHE_TEAMS_DIRECTORY)):
        for file in filenames:
            team_name = file[0:-4] # ignore .txt file extension
            teams[team_name] = []
            with open(
                "{}/{}/{}".format(get_path_cache(), CACHE_TEAMS_DIRECTORY, file), "r", newline="\r\n"
            ) as team_file:
                for line in team_file:
                    teams[team_name] += [line.rstrip("\r\n")]
    return teams
