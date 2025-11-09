import csv
import os
from src.caching import (
    cache_league_objects,
    load_players_stats_map,
    load_rosters,
    load_schedules,
)
from src.constants import (
    KEY_LOSSES,
    KEY_ROSTER,
    KEY_SCHEDULE,
    KEY_STATS,
    KEY_TIES,
    KEY_WINS,
    NINE_CATEGORIES,
    WRITE_RECORD,
    YEAR,
)
from src.env import ESPN_LEAGUE_ID, LOAD_FROM_CACHE, MY_TEAM, USE_HASHTAG
from src.espn_interactions.basketball import (
    build_teamname_to_roster_map,
    construct_players_stats_map,
    extract_schedules_from_league,
    get_league,
)
from src.hashtag import get_player_stat_map_from_hashtag


RESULTS_DIRECTORY = "results"


def combine_rosters_and_schedules(rosters, schedules):
    teams = {}
    for team_name in rosters:
        teams[team_name] = {KEY_ROSTER: rosters[team_name]}
        teams[team_name][KEY_SCHEDULE] = schedules[team_name]
    return teams


def construct_teams_and_stats_map():
    if LOAD_FROM_CACHE:
        rosters = load_rosters()
        schedules = load_schedules()
        players_stats_map = load_players_stats_map()
        if USE_HASHTAG:
            players_stats_map = get_player_stat_map_from_hashtag(players_stats_map)
    else:
        league = get_league(ESPN_LEAGUE_ID, YEAR)

        rosters = build_teamname_to_roster_map(league)
        schedules = extract_schedules_from_league(league)
        players_stats_map = construct_players_stats_map(league)
        if USE_HASHTAG:
            players_stats_map = get_player_stat_map_from_hashtag(players_stats_map)

        cache_league_objects(rosters, schedules, players_stats_map)

    teams = combine_rosters_and_schedules(rosters, schedules)

    return [teams, players_stats_map]


def construct_sorted_teams_stats_map(teams):
    sorted_teams_stats = {}
    for category in NINE_CATEGORIES:
        sorted_teams_stats[category] = []

    for team in teams:
        for category in NINE_CATEGORIES:
            category_count = len(sorted_teams_stats[category])
            team_stat = teams[team][KEY_STATS][category]
            stat_and_team = [team_stat, team]
            if category_count == 0:
                sorted_teams_stats[category].append(stat_and_team)
            else:
                for index in range(category_count):
                    if team_stat > sorted_teams_stats[category][index][0]:
                        sorted_teams_stats[category].insert(index, stat_and_team)
                        break
                    elif index + 1 == category_count:
                        sorted_teams_stats[category].append(stat_and_team)

    return sorted_teams_stats


def teamWinsComparator(team):
    return -team[1][KEY_WINS]


def formatStat(stat, decimalPlaces):
    return str(round(stat, decimalPlaces)).ljust(6)


def print_all_team_stats(teams):
    sorted_teams = sorted(teams.items(), key=teamWinsComparator)

    longest_name_length = 0;
    for team in sorted_teams:
        if len(team[0]) > longest_name_length:
            longest_name_length = len(team[0])

    print("\nTeam".ljust(longest_name_length), " FG%    FT%    3PM    REB    AST    STL    BLK    TO     PTS    Wins")
    for team in sorted_teams:
        print(team[0].ljust(longest_name_length),
              formatStat(team[1][KEY_STATS]['FG%'], 4),
              formatStat(team[1][KEY_STATS]['FT%'], 4),
              formatStat(team[1][KEY_STATS]['3PM'], 1),
              formatStat(team[1][KEY_STATS]['REB'], 1),
              formatStat(team[1][KEY_STATS]['AST'], 1),
              formatStat(team[1][KEY_STATS]['STL'], 1),
              formatStat(team[1][KEY_STATS]['BLK'], 1),
              formatStat(team[1][KEY_STATS]['TO'], 1),
              formatStat(team[1][KEY_STATS]['PTS'], 1),
              team[1][KEY_WINS])


def print_my_team_stat_rankings(teams):
    sorted_teams_stats = construct_sorted_teams_stats_map(teams)
    print(MY_TEAM + " stat rankings:")
    for stat_category in NINE_CATEGORIES:
        for rank in range(len(teams)):
            if sorted_teams_stats[stat_category][rank][1] == MY_TEAM:
                print("{} : {}".format(stat_category, rank + 1))
                break
            elif rank + 1 == len(teams):
                print("not found: {} {}".format(MY_TEAM, stat_category))


def save_projection_to_file(teams):
    os.makedirs(RESULTS_DIRECTORY, exist_ok=True)
    with open(
        "{}/{} - {} projection.csv".format(RESULTS_DIRECTORY, YEAR, ESPN_LEAGUE_ID),
        "w",
        newline="\n",
    ) as results_file:
        writer = csv.writer(results_file)
        headerRow = ["Team"] + NINE_CATEGORIES
        if WRITE_RECORD:
            headerRow += ["Record"]
        else:
            headerRow += [KEY_WINS, KEY_LOSSES, KEY_TIES]
        writer.writerow(headerRow)
        for team in teams:
            row = [team]
            for stat in NINE_CATEGORIES:
                row += [teams[team][KEY_STATS][stat]]
            if WRITE_RECORD:
                row += [
                    "{}-{}-{}".format(
                        teams[team][KEY_WINS],
                        teams[team][KEY_LOSSES],
                        teams[team][KEY_TIES],
                    )
                ]
            else:
                row += [
                    teams[team][KEY_WINS],
                    teams[team][KEY_LOSSES],
                    teams[team][KEY_TIES],
                ]
            writer.writerow(row)
