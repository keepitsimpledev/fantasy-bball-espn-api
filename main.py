from src.processing import construct_teams_and_stats_map
from src.calculations import calculate_team_stats, simulate_season


if __name__ == "__main__":
    [teams, players_stats_map] = construct_teams_and_stats_map()

    calculate_team_stats(teams, players_stats_map)
    simulate_season(teams)

    for team in teams:
        print("team name: " + team)
