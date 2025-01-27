import logging
from src.constants import (
    ALL_STATS,
    NINE_CATEGORIES,
    KEY_SCHEDULE,
    KEY_ROSTER,
    KEY_IR,
    KEY_STATS,
    KEY_WINS,
    KEY_LOSSES,
    KEY_TIES,
)


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
                continue  # TODO check why this is necessary - what does a lack of an IR flag indicate?
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
