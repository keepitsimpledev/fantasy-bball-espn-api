from espn_api.basketball import League, Team
from validation.espn_class_validator import validate_league


def get_league(league_id, year):
    league = League(league_id, year)
    validate_league(league)
    return league


def extract_rosters_from_espn_league(league: League):
    teams = {}
    for team in league.teams:
        name = get_formatted_name_from_espn_team_object(team)
        players = []
        for player in team.roster:
            players += [player.name]
        teams[name] = players
    return teams


def get_formatted_name_from_espn_team_object(espn_team: Team):
    return (
        "{} ({})".format(espn_team.team_name, espn_team.team_abbrev)
        .replace("?", "")
        .replace("⭐", "")
    )
