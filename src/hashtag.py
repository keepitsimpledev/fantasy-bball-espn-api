import csv
from src.constants import KEY_IR
import logging


logger = logging.getLogger(__name__)


HASHTAG_STATS_FILE = "hashtagbasketball/stats.csv"


def get_player_stat_map_from_hashtag(players_stats_map):
    hashtag_players_stats_map = get_stats()
    for hashtag_player in hashtag_players_stats_map:
        if hashtag_player in players_stats_map:
            hashtag_players_stats_map[hashtag_player][KEY_IR] = players_stats_map[hashtag_player][KEY_IR]
        else:
            print("player not found in ESPN: " + hashtag_player)
    return hashtag_players_stats_map


def get_stats():
    all_players_stats_map = {}
    # stats.csv created from copying the table from hashtagbasketball and pasting into a UTF8 spreadsheet
    # and players names have been updated to match ESPN, where necessary
    with open(
        HASHTAG_STATS_FILE, "r", newline="\n", encoding="utf8"
    ) as stats_file:
        reader = csv.DictReader(stats_file)
        for row in reader:
            if row["R#"] == "R#":
                continue
            player_name = to_espn_name(row["PLAYER"])
            [fgm, fga] = percent_to_made_and_total(row["FG%"])
            [ftm, fta] = percent_to_made_and_total(row["FT%"])
            all_players_stats_map[player_name] = {
                "FGM": float(fgm),
                "FGA": float(fga),
                "FTM": float(ftm),
                "FTA": float(fta),
                "3PM": float(row["3PM"]),
                "REB": float(row["TREB"]),
                "AST": float(row["AST"]),
                "STL": float(row["STL"]),
                "BLK": float(row["BLK"]),
                "PTS": float(row["PTS"]),
                "TO": float(row["TO"]),
            }
    return all_players_stats_map


# assumption: percent is in the format `FG% (FGM/FGA)`, example: `0.624 (9.9/15.9)`
def percent_to_made_and_total(percent):
    made_and_attemped = percent.split(" ")
    [made, attempted] = made_and_attemped[1].split("/")
    made = made[1:]
    attempted = attempted[: len(attempted) - 1]
    return [float(made), float(attempted)]


# to align hashtag names with ESPN names
def to_espn_name(hashtag_name):
    if hashtag_name == "Nicolas Claxton":
        return "Nic Claxton"
    elif hashtag_name == "Alperen Sengn" or hashtag_name == "Alperen Sengün":
        return "Alperen Sengun"
    elif hashtag_name == "Dennis Schr”der" or hashtag_name == "Dennis Schröder":
        return "Dennis Schroder"
    elif hashtag_name == "Xavier Tillman Sr.":
        return "Xavier Tillman"
    elif hashtag_name == "Reggie Bullock":
        return "Reggie Bullock Jr."
    elif hashtag_name == "Aleksandar Vezenkov":
        return "Sasha Vezenkov"
    elif hashtag_name == "Th‚o Maledon" or hashtag_name == "Théo Maledon":
        return "Theo Maledon"
    elif hashtag_name == "™mer Yurtseven" or hashtag_name == "Ömer Yurtseven":
        return "Omer Yurtseven"
    elif hashtag_name == "Patrick Baldwin Jr.":
        return "Patrick Baldwin"
    elif hashtag_name == "Andre Jackson":
        return "Andre Jackson Jr."
    elif hashtag_name == "EJ Liddell":
        return "E.J. Liddell"
    elif hashtag_name == "Alexandre Sarr":
        return "Alex Sarr"
    return hashtag_name
