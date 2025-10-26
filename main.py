from src.calculations import calculate_team_stats, simulate_season
from src.env import MY_TEAM
from src.processing import construct_teams_and_stats_map, print_my_team_stats, save_projection_to_file
from src.transactions import add, drop, trade


def process_transactions(teams, players_stats_map):
    drop("Keyonte George", teams)
    add("Mike Conley", MY_TEAM, players_stats_map, teams)
    trade(["James Harden", "Kelly Oubre Jr."], ["Stephen Curry", "Deni Avdija"], teams)


if __name__ == "__main__":
    [teams, players_stats_map] = construct_teams_and_stats_map()
    calculate_team_stats(teams, players_stats_map)

    # process_transactions(teams, players_stats_map)

    simulate_season(teams)
    print_my_team_stats(teams)
    save_projection_to_file(teams)
