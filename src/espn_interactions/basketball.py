from src.constants import ALL_STATS, ESPN_STATS_KEY, ESPN_STATS_TOTAL_KEY, KEY_IR
from espn_api.basketball import League, Team
from src.validation.espn_class_validator import validate_league
import logging

logger = logging.getLogger(__name__)


def get_league(league_id, year):
    league = League(league_id, year)
    validate_league(league)
    return league


def build_teamname_to_roster_map(league: League):
    name_to_roster_map = {}
    for team in league.teams:
        name = format_team_name(team)
        players = []
        for player in team.roster:
            players += [player.name]
        name_to_roster_map[name] = players
    return name_to_roster_map


def extract_all_players_from_league(league: League):
    all_players = []
    for team in league.teams:
        all_players += team.roster
    free_agents = league.free_agents(size=1000)
    all_players += free_agents
    return all_players


# todo: add a comment for this function indicating what this function solves
def format_team_name(team: Team):
    formatted_name = ""
    if not hasattr(team, "team_abbrev") or len(team.team_abbrev) < 1:
        formatted_name = team.team_name
    else:
        formatted_name = "{} ({})".format(team.team_name, team.team_abbrev)
    return formatted_name.replace("?", "").replace("⭐", "")


def construct_players_stats_map(league: League):
    all_espn_player_objects = extract_all_players_from_league(league)
    all_players_stat_map = {}
    for player in all_espn_player_objects:
        all_players_stat_map[player.name] = {}
        projections_not_found = []
        for stat in ALL_STATS:
            if (
                ESPN_STATS_KEY in player.stats
                and ESPN_STATS_TOTAL_KEY in player.stats[ESPN_STATS_KEY] # noqa: W504
                and stat in player.stats[ESPN_STATS_KEY][ESPN_STATS_TOTAL_KEY] # noqa: W504
            ):
                value = player.stats[ESPN_STATS_KEY][ESPN_STATS_TOTAL_KEY][stat]
                all_players_stat_map[player.name][stat] = int(value)
            else:
                # previously we used previous year's average, but that seems to now be unavailable in the ESPN API
                projections_not_found.append(stat)
                all_players_stat_map[player.name][stat] = 0
        all_players_stat_map[player.name][KEY_IR] = player.lineupSlot == "IR"
        if len(projections_not_found) > 0:
            logger.info(
                "{} projections not found: {}".format(
                    player.name, ", ".join(projections_not_found)
                )
            )
    return all_players_stat_map
