from src.caching import (
    cache_league_objects,
    load_players_stats_map,
    load_rosters,
    load_schedules,
)
from src.constants import (
    ESPN_LEAGUE_ID,
    YEAR,
    KEY_IR,
    KEY_STATS,
    KEY_ROSTER,
    KEY_SCHEDULE,
    LOAD_FROM_CACHE,
    MY_TEAM,
    NINE_CATEGORIES,
)
from src.espn_interactions.basketball import (
    build_teamname_to_roster_map,
    construct_players_stats_map,
    extract_schedules_from_league,
    get_league,
)


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
    else:
        league = get_league(ESPN_LEAGUE_ID, YEAR)

        rosters = build_teamname_to_roster_map(league)
        schedules = extract_schedules_from_league(league)
        players_stats_map = construct_players_stats_map(league)

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


def print_my_team_stats(teams):
    sorted_teams_stats = construct_sorted_teams_stats_map(teams)
    print(MY_TEAM + " stat rankings:")
    for stat_category in NINE_CATEGORIES:
        for rank in range(len(teams)):
            if sorted_teams_stats[stat_category][rank][1] == MY_TEAM:
                print("{} : {}".format(stat_category, rank + 1))
                break
            elif rank + 1 == len(teams):
                print("not found: {} {}".format(MY_TEAM, stat_category))
