from src.processing import construct_teams_and_stats_map


if __name__ == "__main__":
    [teams, players_stats_map] = construct_teams_and_stats_map()

    for team in teams:
        print("team name: " + team)
