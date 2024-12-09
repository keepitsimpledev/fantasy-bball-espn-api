from constants import ESPN_LEAGUE_ID, YEAR
from espn_interactions.basketball import get_league


if __name__ == "__main__":
    league = get_league(ESPN_LEAGUE_ID, YEAR)
    name = league.settings.name
    print("league name: " + name)
