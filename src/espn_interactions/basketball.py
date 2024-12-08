from espn_api.basketball import League


def get_league_from_espn(league_id, year):
    return League(league_id, year)
