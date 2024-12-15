from src.constants import ESPN_LEAGUE_ID, YEAR
from src.espn_interactions.basketball import get_league, construct_players_stats_map


if __name__ == "__main__":
    league = get_league(ESPN_LEAGUE_ID, YEAR)

    stat_map = construct_players_stats_map(league)

    name = league.settings.name
    print("league name: " + name)
