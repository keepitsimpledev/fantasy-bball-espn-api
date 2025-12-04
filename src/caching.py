import csv
import os
import shutil
from src.constants import ALL_STATS, CACHE_HEADER_PLAYER, KEY_IR, KEY_POSITION
from src.env import ESPN_LEAGUE_ID
from src.espn_interactions.basketball import remove_unallowed_characters


CACHE_DIRECTORY = "cached"
CACHE_TEAMS_DIRECTORY = "teams"
CACHE_SCHEDULES_DIRECTORY = "schedules"


def get_path_cache():
    return "{}/{}/".format(CACHE_DIRECTORY, ESPN_LEAGUE_ID)


def cache_league_objects(rosters, schedules, players_stats_map):
    init_cache_folders()
    cache_rosters(rosters)
    cache_schedules(schedules)
    cache_players_stats_map(players_stats_map)


def init_cache_folders():
    if os.path.exists(get_path_cache()):
        shutil.rmtree(get_path_cache())
    os.makedirs(get_path_cache() + CACHE_TEAMS_DIRECTORY, exist_ok=True)
    os.makedirs(get_path_cache() + CACHE_SCHEDULES_DIRECTORY, exist_ok=True)


def cache_rosters(rosters):
    for team_name in rosters:
        team_name_encoded = remove_unallowed_characters(team_name)
        with open(
            "{}/{}/{}.csv".format(
                get_path_cache(), CACHE_TEAMS_DIRECTORY, team_name_encoded
            ),
            "w",
            newline="\n",
        ) as team_file:
            writer = csv.writer(team_file)
            for player in rosters[team_name]:
                writer.writerow([player])


def cache_players_stats_map(players_stats_map):
    with open(
        "{}/players.csv".format(get_path_cache()), "w", newline="\n"
    ) as players_file:
        writer = csv.DictWriter(
            players_file,
            fieldnames=[CACHE_HEADER_PLAYER] + [KEY_POSITION] + ALL_STATS + [KEY_IR],
        )
        writer.writeheader()
        for player_name in players_stats_map:
            players_stats_map[player_name][CACHE_HEADER_PLAYER] = player_name
            writer.writerow(players_stats_map[player_name])


def cache_schedules(schedules):
    for team_name in schedules:
        team_name_encoded = remove_unallowed_characters(team_name)
        with open(
            "{}/{}/{}.csv".format(
                get_path_cache(), CACHE_SCHEDULES_DIRECTORY, team_name_encoded
            ),
            "w",
            newline="\n",
        ) as schedule_file:
            writer = csv.writer(schedule_file)
            for opponent in schedules[team_name]:
                writer.writerow([opponent])


def load_rosters():
    rosters = {}
    for __, __, filenames in os.walk(
        "./{}/{}/".format(get_path_cache(), CACHE_TEAMS_DIRECTORY)
    ):
        if len(filenames) < 2:
            raise CachingError(
                "expected multiple team files but found {}".format(len(filenames))
            )
        for file in filenames:
            team_name = file[0:-4]  # ignore .csv file extension
            rosters[team_name] = []
            with open(
                "{}/{}/{}".format(get_path_cache(), CACHE_TEAMS_DIRECTORY, file),
                "r",
                newline="\r\n",
            ) as team_file:
                for line in team_file:
                    rosters[team_name] += [line.rstrip("\r\n")]
            if len(rosters[team_name]) < 2:
                raise CachingError(
                    "expected multiple players for team {} but found {}".format(
                        team_name, len(rosters[team_name])
                    )
                )
    return rosters


def load_players_stats_map():
    all_players = {}
    with open(
        "{}/players.csv".format(get_path_cache()), "r", newline="\n"
    ) as players_file:
        reader = csv.DictReader(players_file)
        for row in reader:
            all_players[row[CACHE_HEADER_PLAYER]] = {}
            for stat in ALL_STATS:
                all_players[row[CACHE_HEADER_PLAYER]][stat] = int(float(row[stat]))
            all_players[row[CACHE_HEADER_PLAYER]][KEY_IR] = row[KEY_IR]
    if len(all_players) < 200:
        raise CachingError(
            "expected no less than 350 players but found {}".format(len(all_players))
        )
    return all_players


def load_schedules():
    schedules = {}
    for __, __, filenames in os.walk(
        "./{}/{}/".format(get_path_cache(), CACHE_SCHEDULES_DIRECTORY)
    ):
        for file in filenames:
            team_name = file[0:-4]
            schedules[team_name] = []
            with open(
                "{}/{}/".format(get_path_cache(), CACHE_SCHEDULES_DIRECTORY) + file,
                "r",
                newline="\r\n",
            ) as team_schedule:
                for line in team_schedule:
                    schedules[team_name] += [line.rstrip("\r\n")]
    return schedules


class CachingError(Exception):
    def __init__(self, message):
        super(CachingError, self).__init__(message)
        self.message = message
