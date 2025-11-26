import copy
import logging
from src.constants import (
    ALL_STATS,
    NINE_CATEGORIES,
    KEY_POSITION,
    KEY_IR,
    KEY_ROSTER,
    KEY_SCHEDULE,
    KEY_STATS,
    KEY_WINS,
    KEY_LOSSES,
    KEY_TIES,
)
from src.env import MY_TEAM
from src.transactions import add, drop


logger = logging.getLogger(__name__)


def calculate_team_stats(teams, players_stats_map):
    for team in teams:
        teams[team][KEY_STATS] = {}
        team_stats = teams[team][KEY_STATS]
        for stat in ALL_STATS:
            team_stats[stat] = 0
        for player in teams[team][KEY_ROSTER]:
            if player not in players_stats_map:
                logger.warning("stats not found for {}".format(player))
                continue
            if KEY_IR not in players_stats_map[player]:
                # raise Exception(
                #     "TODO check why this is necessary - what does a lack of an IR flag indicate?"
                # ) # one reason: hashtag player not found causes missing KEY_IR
                continue
            if players_stats_map[player][KEY_IR] == "True":
                continue  # IR players won't contribute to calculations
            for stat in ALL_STATS:
                team_stats[stat] += players_stats_map[player][stat]
        fg_pct = team_stats["FGM"] / team_stats["FGA"]
        ft_pct = team_stats["FTM"] / team_stats["FTA"]
        del team_stats["FGM"], team_stats["FGA"], team_stats["FTM"], team_stats["FTA"]
        team_stats["FG%"] = round(fg_pct, 4)
        team_stats["FT%"] = round(ft_pct, 4)
        team_stats["TO"] = team_stats["TO"] * -1


def simulate_season(teams):
    for team_name in teams:
        wins = losses = ties = 0
        team_stats = teams[team_name][KEY_STATS]
        for matchup in teams[team_name][KEY_SCHEDULE]:
            opponent_stats = teams[matchup][KEY_STATS]
            for stat in NINE_CATEGORIES:
                if team_stats[stat] > opponent_stats[stat]:
                    wins += 1
                elif team_stats[stat] < opponent_stats[stat]:
                    losses += 1
                else:
                    ties += 1
        teams[team_name][KEY_WINS] = wins
        teams[team_name][KEY_LOSSES] = losses
        teams[team_name][KEY_TIES] = ties


def scored_transaction_comparator(st):
    return -st.score


class ScoredTransaction:
    def __init__(self, score, drop, add=None):
        self.score = score
        self.drop = drop
        self.add = add


def compare_waiver_moves(teams, all_players_stats):
    print("\npotential moves:")
    calculate_team_stats(teams, all_players_stats)
    simulate_season(teams)
    original_roster = copy.deepcopy(teams[MY_TEAM][KEY_ROSTER])
    original_win_count = teams[MY_TEAM][KEY_WINS]

    do_not_add_players = ["Walker Kessler", "Jayson Tatum", "Kawhi Leonard"]
    do_not_add_positions = ["C"]
    rostered_players = []
    for team in teams:
        for player in teams[team][KEY_ROSTER]:
            rostered_players.append(player)

    scored_transactions = []
    for player_to_drop in teams[MY_TEAM][KEY_ROSTER]:
        if all_players_stats[player_to_drop][KEY_IR] == 'True':
            continue
        teams[MY_TEAM][KEY_ROSTER] = copy.deepcopy(original_roster)
        drop(player_to_drop, teams)
        roster_after_drop = copy.deepcopy(teams[MY_TEAM][KEY_ROSTER])
        for fa_to_add in all_players_stats:
            if fa_to_add in rostered_players:
                continue
            if fa_to_add in do_not_add_players:
                continue
            if all_players_stats[fa_to_add][KEY_POSITION] in do_not_add_positions:
                continue
            teams[MY_TEAM][KEY_ROSTER] = copy.deepcopy(roster_after_drop)
            add(fa_to_add, MY_TEAM, all_players_stats, teams)
            calculate_team_stats(teams, all_players_stats)
            simulate_season(teams)
            current_win_count = teams[MY_TEAM][KEY_WINS]
            scored_transactions.append(
                ScoredTransaction(
                    current_win_count - original_win_count,
                    player_to_drop,
                    fa_to_add,
                )
            )

    sorted_transactions = sorted(scored_transactions, key=scored_transaction_comparator)
    num_to_reveal = 25 if len(sorted_transactions) > 25 else len(sorted_transactions)
    for i in range(num_to_reveal):
        t = sorted_transactions[i]
        print("{} win(s): drop {} add {}".format(t.score, t.drop, t.add))

    teams[MY_TEAM][KEY_ROSTER] = original_roster


def determine_worst_player(teams, all_players_stats):
    print("\nworst players:")
    calculate_team_stats(teams, all_players_stats)
    simulate_season(teams)
    original_roster = copy.deepcopy(teams[MY_TEAM][KEY_ROSTER])
    original_win_count = teams[MY_TEAM][KEY_WINS]

    scored_transactions = []
    for player_to_drop in teams[MY_TEAM][KEY_ROSTER]:
        if all_players_stats[player_to_drop][KEY_IR] == 'True':
            continue
        teams[MY_TEAM][KEY_ROSTER] = copy.deepcopy(original_roster)
        drop(player_to_drop, teams)
        calculate_team_stats(teams, all_players_stats)
        simulate_season(teams)
        current_win_count = teams[MY_TEAM][KEY_WINS]
        scored_transactions.append(
            ScoredTransaction(
                current_win_count - original_win_count,
                player_to_drop,
            )
        )

    sorted_transactions = sorted(scored_transactions, key=scored_transaction_comparator)
    for i in range(len(sorted_transactions)):
        t = sorted_transactions[i]
        print("{} win(s) after dropping {}".format(t.score, t.drop))

    teams[MY_TEAM][KEY_ROSTER] = original_roster
