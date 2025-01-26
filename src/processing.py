from src.caching import (
    cache_teams,
    init_cache_folders,
    load_players_stats_map,
    load_teams,
)
from src.constants import (
    ESPN_LEAGUE_ID,
    YEAR,
    KEY_ROSTER,
    KEY_SCHEDULE,
    LOAD_FROM_CACHE,
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
    league = get_league(ESPN_LEAGUE_ID, YEAR)

    rosters = build_teamname_to_roster_map(league)
    schedule = extract_schedules_from_league(league)
    if LOAD_FROM_CACHE:
        teams = load_teams()

        players_stats_map = load_players_stats_map()
    else:
        init_cache_folders()

        teams = combine_rosters_and_schedules(rosters, schedule)
        cache_teams(teams)

        players_stats_map = construct_players_stats_map(league)

    return [teams, players_stats_map]
