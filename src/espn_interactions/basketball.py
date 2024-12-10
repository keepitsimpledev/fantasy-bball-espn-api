from espn_api.basketball import League, Team
from src.validation.espn_class_validator import validate_league


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


# todo: add a comment for this function indicating what this function solves
def format_team_name(team: Team):
    formatted_name = ""
    if not hasattr(team, "team_abbrev") or len(team.team_abbrev) < 1:
        formatted_name = team.team_name
    else:
        formatted_name = "{} ({})".format(team.team_name, team.team_abbrev)
    return formatted_name.replace("?", "").replace("⭐", "")
