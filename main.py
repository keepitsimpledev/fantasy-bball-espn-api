from src.calculations import (
    calculate_team_stats,
    compare_waiver_moves,
    determine_worst_player,
    simulate_season,
)
from src.env import MY_TEAM
from src.logging import get_logger
from src.processing import (
    construct_teams_and_stats_map,
    print_my_team_stat_rankings,
    print_all_team_stats,
    save_projection_to_file,
)
from src.transactions import add, drop, trade


logger = get_logger(__name__)


def process_transactions(teams, players_stats_map):
    logger.info("")
    logger.info("processing transactions:")
    drop("Keyonte George", teams)
    add("Mike Conley", MY_TEAM, players_stats_map, teams)
    trade(["James Harden", "Kelly Oubre Jr."], ["Stephen Curry", "Deni Avdija"], teams)


if __name__ == "__main__":
    [teams, players_stats_map] = construct_teams_and_stats_map()

    calculate_team_stats(teams, players_stats_map)
    simulate_season(teams)
    print_all_team_stats(teams)
    print_my_team_stat_rankings(teams)

    process_transactions(teams, players_stats_map)
    calculate_team_stats(teams, players_stats_map)
    simulate_season(teams)
    print_all_team_stats(teams)
    print_my_team_stat_rankings(teams)

    compare_waiver_moves(teams, players_stats_map)
    determine_worst_player(teams, players_stats_map)

    save_projection_to_file(teams)
