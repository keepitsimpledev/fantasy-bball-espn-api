import copy
from src.logging import get_logger
import src.transactions as transactions
from src.constants import (
    ALL_STATS,
    NINE_CATEGORIES,
    KEY_CONTRIBUTIONS,
    KEY_POSITION,
    KEY_IR,
    KEY_ROSTER,
    KEY_SCHEDULE,
    KEY_STATS,
    KEY_WINS,
    KEY_LOSSES,
    KEY_TIES,
)
from src.env import DO_NOT_ADD, DO_NOT_DROP, MAX_POSITIONS, MY_TEAM
from src.transactions import add, drop


logger = get_logger(__name__)

LOG_MISSING_PLAYER = True


def calculate_team_stats(teams, players_stats_map):
    missing_players = []
    for team in teams:
        teams[team][KEY_STATS] = {}
        team_stats = teams[team][KEY_STATS]
        for stat in ALL_STATS:
            team_stats[stat] = 0
        for player in teams[team][KEY_ROSTER]:
            if player not in players_stats_map:
                missing_players.append(player)
                continue
            if KEY_IR not in players_stats_map[player]:
                # raise Exception(
                #     "TODO check why this is necessary - what does a lack of an IR flag indicate?"
                # ) # one reason: hashtag player not found causes missing KEY_IR
                continue
            if (
                players_stats_map[player][KEY_IR] == "True"  # is a string from cached spreadsheet
                or players_stats_map[player][KEY_IR] == True  # noqa: E712 | is boolean from ESPN
            ):
                continue  # IR players won't contribute to calculations
            for stat in ALL_STATS:
                team_stats[stat] += players_stats_map[player][stat]
        fg_pct = team_stats["FGM"] / team_stats["FGA"]
        ft_pct = team_stats["FTM"] / team_stats["FTA"]
        del team_stats["FGM"], team_stats["FGA"], team_stats["FTM"], team_stats["FTA"]
        team_stats["FG%"] = round(fg_pct, 4)
        team_stats["FT%"] = round(ft_pct, 4)
        team_stats["TO"] = team_stats["TO"] * -1
    global LOG_MISSING_PLAYER
    if LOG_MISSING_PLAYER:
        for player in missing_players:
            logger.warning("stats not found for {}".format(player))


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
    originalLogTransactions = transactions.LOG_TRANSACTIONS
    transactions.LOG_TRANSACTIONS = False
    global LOG_MISSING_PLAYER
    originalLogMissingPlayer = LOG_MISSING_PLAYER
    LOG_MISSING_PLAYER = False

    logger.info("")
    logger.info("potential moves:")
    calculate_team_stats(teams, all_players_stats)
    simulate_season(teams)
    original_roster = copy.deepcopy(teams[MY_TEAM][KEY_ROSTER])
    original_win_count = teams[MY_TEAM][KEY_WINS]

    do_not_add_players = DO_NOT_ADD
    do_not_drop_players = DO_NOT_DROP
    rostered_players = []
    for team in teams:
        for player in teams[team][KEY_ROSTER]:
            rostered_players.append(player)

    scored_transactions = []
    for player_to_drop in teams[MY_TEAM][KEY_ROSTER]:
        if player_to_drop in do_not_drop_players:
            logger.info("skipping {} from do-not-drop list".format(player_to_drop))
            continue
        if (
            all_players_stats[player_to_drop][KEY_IR] == "True"  # is a string in cached spreadsheet
            or all_players_stats[player_to_drop][KEY_IR] == True  # noqa: E712 | is boolean from ESPN
        ):
            continue
        teams[MY_TEAM][KEY_ROSTER] = copy.deepcopy(original_roster)
        drop(player_to_drop, teams)
        roster_after_drop = copy.deepcopy(teams[MY_TEAM][KEY_ROSTER])
        for fa_to_add in all_players_stats:
            if fa_to_add in rostered_players:
                continue
            if fa_to_add in do_not_add_players:
                logger.info("skipping {} from do-not-add list".format(fa_to_add))
                continue

            teams[MY_TEAM][KEY_ROSTER] = copy.deepcopy(roster_after_drop)
            add(fa_to_add, MY_TEAM, all_players_stats, teams)

            skip_due_to_too_many_of_position = False  # TODO: test
            count_team_positions(MY_TEAM, teams, all_players_stats)
            for position in MAX_POSITIONS:
                if (
                    position in teams[MY_TEAM][KEY_POSITION]
                    and teams[MY_TEAM][KEY_POSITION][position] > MAX_POSITIONS[position]
                ):
                    skip_due_to_too_many_of_position = True
                    break
            if skip_due_to_too_many_of_position:
                skip_due_to_too_many_of_position = False
                continue

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
        logger.info("{} win(s): drop {} add {}".format(t.score, t.drop, t.add))

    teams[MY_TEAM][KEY_ROSTER] = original_roster
    transactions.LOG_TRANSACTIONS = originalLogTransactions
    LOG_MISSING_PLAYER = originalLogMissingPlayer


def determine_worst_player(teams, all_players_stats):
    originalLogTransactions = transactions.LOG_TRANSACTIONS
    transactions.LOG_TRANSACTIONS = False
    global LOG_MISSING_PLAYER
    originalLogMissingPlayer = LOG_MISSING_PLAYER
    LOG_MISSING_PLAYER = False

    logger.info("")
    logger.info("worst players:")
    calculate_team_stats(teams, all_players_stats)
    simulate_season(teams)
    original_roster = copy.deepcopy(teams[MY_TEAM][KEY_ROSTER])
    original_win_count = teams[MY_TEAM][KEY_WINS]

    scored_transactions = []
    for player_to_drop in teams[MY_TEAM][KEY_ROSTER]:
        if (
            all_players_stats[player_to_drop][KEY_IR] == "True"  # is a string in cached spreadsheet
            or all_players_stats[player_to_drop][KEY_IR] == True  # noqa: E712 | is boolean from ESPN
        ):
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
        logger.info("{} win(s) after dropping {}".format(t.score, t.drop))

    teams[MY_TEAM][KEY_ROSTER] = original_roster
    transactions.LOG_TRANSACTIONS = originalLogTransactions
    LOG_MISSING_PLAYER = originalLogMissingPlayer


def count_team_positions(team_name, teams, all_players_stats):
    position_map = {}
    for player in teams[team_name][KEY_ROSTER]:
        players_position = get_primary_position(all_players_stats[player][KEY_POSITION])
        if players_position in position_map:
            position_map[players_position] += 1
        else:
            position_map[players_position] = 1
    teams[team_name][KEY_POSITION] = position_map


def get_primary_position(position):
    position_out = ""
    if position[0:1] == "C":
        position_out = "C"
    else:
        position_out = position[0:2]
    return position_out


def calculate_team_contributions(team, all_players_stats):
    contributions = {}
    for player in team[KEY_ROSTER]:
        team_stats = team[KEY_STATS]
        player_stats = all_players_stats[player]
        contributions[player] = {}

        fgm_without = team_stats["FGM"] - player_stats["FGM"]
        fga_without = team_stats["FGA"] - player_stats["FGA"]
        fg_without = fgm_without / fga_without
        contributions[player]["FG%"] = round(team_stats["FG%"] - fg_without, 4)

        ftm_without = team_stats["FTM"] - player_stats["FTM"]
        fta_without = team_stats["FTA"] - player_stats["FTA"]
        ft_without = ftm_without / fta_without
        contributions[player]["FT%"] = round(team_stats["FT%"] - ft_without, 4)
    
    team[KEY_CONTRIBUTIONS] = contributions

