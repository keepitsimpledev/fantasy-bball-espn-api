import os
import shutil
from src.constants import ESPN_LEAGUE_ID


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
