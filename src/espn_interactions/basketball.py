from espn_api.basketball import League
from validation.espn_class_validator import validate_league


def get_league(league_id, year):
    league = League(league_id, year)
    validate_league(league)
    return league
