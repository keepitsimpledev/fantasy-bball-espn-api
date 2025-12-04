import src.calculations as calculations
from src.calculations import (
    calculate_team_stats,
    compare_waiver_moves,
    count_team_positions,
    determine_worst_player,
    get_primary_position,
    simulate_season,
)

import unittest


class TestCalcuations(unittest.TestCase):

    def test_calculate_team_stats(self):
        # arrange
        teamA = ["playerA", "playerB"]
        teamB = ["playerC", "playerD", "playerE"]
        teams = {}
        teams["teamA"] = {}
        teams["teamA"]["roster"] = teamA
        teams["teamB"] = {}
        teams["teamB"]["roster"] = teamB
        # reduce stats to simplify test:
        calculations.ALL_STATS = ["FGM", "FGA", "FTM", "FTA", "REB", "TO", "PTS"]

        players_stats_map = {}
        players_stats_map["playerA"] = {
            "FGM": 12,
            "FGA": 24,
            "FTM": 5,
            "FTA": 10,
            "REB": 6,
            "TO": 2,
            "PTS": 27,
            "On IR": "False",
        }
        players_stats_map["playerB"] = {
            "FGM": 4,
            "FGA": 10,
            "FTM": 7,
            "FTA": 8,
            "REB": 2,
            "TO": 4,
            "PTS": 17,
            "On IR": "False",
        }
        players_stats_map["playerC"] = {
            "FGM": 3,
            "FGA": 4,
            "FTM": 6,
            "FTA": 12,
            "REB": 10,
            "TO": 3,
            "PTS": 12,
            "On IR": "False",
        }
        players_stats_map["playerD"] = {
            "FGM": 12,
            "FGA": 30,
            "FTM": 11,
            "FTA": 13,
            "REB": 3,
            "TO": 5,
            "PTS": 42,
            "On IR": "True",
        }

        # act
        with self.assertLogs("src.calculations", level="WARNING") as cm:
            calculate_team_stats(teams, players_stats_map)

        # assert
        self.assertEqual(teams["teamA"]["stats"]["FG%"], 0.4706)
        self.assertEqual(teams["teamA"]["stats"]["FT%"], 0.6667)
        self.assertEqual(teams["teamA"]["stats"]["REB"], 8)
        self.assertEqual(teams["teamA"]["stats"]["TO"], -6)
        self.assertEqual(teams["teamA"]["stats"]["PTS"], 44)

        self.assertEqual(teams["teamB"]["stats"]["FG%"], 0.7500)
        self.assertEqual(teams["teamB"]["stats"]["FT%"], 0.5000)
        self.assertEqual(teams["teamB"]["stats"]["REB"], 10)
        self.assertEqual(teams["teamB"]["stats"]["TO"], -3)
        self.assertEqual(teams["teamB"]["stats"]["PTS"], 12)

        self.assertEqual(
            cm.output[0],
            "WARNING:src.calculations:stats not found for playerE",
        )

    def test_simulate_season(self):
        # arrange
        teams = {}
        teams["teamA"] = {}
        teams["teamA"]["stats"] = {
            "REB": 10,
            "TO": -1,
            "PTS": 10,
        }
        teams["teamA"]["schedule"] = ["teamB", "teamC"]

        teams["teamB"] = {}
        teams["teamB"]["stats"] = {
            "REB": 5,
            "TO": -5,
            "PTS": 20,
        }
        teams["teamB"]["schedule"] = ["teamA", "teamC"]

        teams["teamC"] = {}
        teams["teamC"]["stats"] = {
            "REB": 5,
            "TO": -10,
            "PTS": 5,
        }
        teams["teamC"]["schedule"] = ["teamA", "teamB"]
        # reduce stats to simplify test:
        calculations.NINE_CATEGORIES = ["REB", "TO", "PTS"]

        # act
        simulate_season(teams)

        # assert
        teams["teamA"]["wins"] = 5
        teams["teamA"]["losses"] = 1
        teams["teamA"]["ties"] = 0

        teams["teamB"]["wins"] = 3
        teams["teamB"]["losses"] = 2
        teams["teamB"]["ties"] = 1

        teams["teamC"]["wins"] = 0
        teams["teamC"]["losses"] = 5
        teams["teamC"]["ties"] = 1

    def test_compare_waiver_moves(self):
        # arrange

        # reduce stats to simplify test:
        calculations.ALL_STATS = ["FGM", "FGA", "FTM", "FTA", "TO", "PTS"]
        calculations.NINE_CATEGORIES = ["FG%", "FT%", "TO", "PTS"]

        calculations.DO_NOT_ADD = ["playerG"]
        calculations.DO_NOT_DROP = ["playerB"]

        calculations.MY_TEAM = "teamA"
        teams = {}
        teams["teamA"] = {}
        teams["teamA"]["schedule"] = ["teamB"]
        teams["teamA"]["roster"] = ["playerA", "playerB"]
        teams["teamA"]["stats"] = {
            "FG%": 0.25,
            "FT%": 0.25,
            "PTS": 6,
            "TO": 6,
        }

        teams["teamB"] = {}
        teams["teamB"]["schedule"] = ["teamA"]
        teams["teamB"]["roster"] = ["playerC", "playerD"]
        teams["teamB"]["stats"] = {
            "FG%": 0.5,
            "FT%": 0.5,
            "PTS": 24,
            "TO": 8,
        }

        players_stats_map = {}
        players_stats_map["playerA"] = {
            "position": "PG",
            "FGM": 1,
            "FGA": 4,
            "FTM": 1,
            "FTA": 4,
            "TO": 3,
            "PTS": 3,
            "On IR": "False",
        }
        players_stats_map["playerB"] = {
            "position": "PG",
            "FGM": 1,
            "FGA": 4,
            "FTM": 1,
            "FTA": 4,
            "TO": 4,
            "PTS": 3,
            "On IR": "False",
        }
        players_stats_map["playerC"] = {
            "position": "C",
            "FGM": 4,
            "FGA": 8,
            "FTM": 4,
            "FTA": 8,
            "TO": 4,
            "PTS": 12,
            "On IR": "False",
        }
        players_stats_map["playerD"] = {
            "position": "C",
            "FGM": 4,
            "FGA": 8,
            "FTM": 4,
            "FTA": 8,
            "TO": 4,
            "PTS": 12,
            "On IR": "False",
        }
        players_stats_map["playerE"] = {
            "position": "SF",
            "FGM": 10,
            "FGA": 10,
            "FTM": 10,
            "FTA": 10,
            "TO": 0,
            "PTS": 30,
            "On IR": "False",
        }
        players_stats_map["playerF"] = {
            "position": "PF",
            "FGM": 0,
            "FGA": 5,
            "FTM": 0,
            "FTA": 10,
            "TO": 10,
            "PTS": 0,
            "On IR": "False",
        }
        players_stats_map["playerG"] = {
            "position": "SF",
            "FGM": 10,
            "FGA": 10,
            "FTM": 10,
            "FTA": 10,
            "TO": 0,
            "PTS": 40,
            "On IR": "False",
        }

        # act
        with self.assertLogs(calculations.logger, level='INFO') as captured_logs:
            compare_waiver_moves(teams, players_stats_map)

        # assert
        self.assertEqual(
            captured_logs.output,
            [
                'INFO:src.calculations:',
                'INFO:src.calculations:potential moves:',
                'INFO:src.calculations:skipping playerG from do-not-add list',
                'INFO:src.calculations:skipping playerB from do-not-drop list',
                'INFO:src.calculations:3 win(s): drop playerA add playerE',
                'INFO:src.calculations:-1 win(s): drop playerA add playerF',
            ]
        )

    def test_compare_waiver_moves_max_position(self):
        # arrange

        calculations.MAX_POSITIONS = {"C": 0}

        # reduce stats to simplify test:
        calculations.ALL_STATS = ["FGM", "FGA", "FTM", "FTA", "TO", "PTS"]
        calculations.NINE_CATEGORIES = ["FG%", "FT%", "TO", "PTS"]

        calculations.MY_TEAM = "teamA"
        teams = {}
        teams["teamA"] = {}
        teams["teamA"]["schedule"] = ["teamB"]
        teams["teamA"]["roster"] = ["playerA"]
        teams["teamA"]["stats"] = {
            "FG%": 0.0,
            "FT%": 0.0,
            "PTS": 0,
            "TO": 5,
        }

        teams["teamB"] = {}
        teams["teamB"]["schedule"] = ["teamA"]
        teams["teamB"]["roster"] = ["playerB"]
        teams["teamB"]["stats"] = {
            "FG%": 0.5,
            "FT%": 0.5,
            "PTS": 3,
            "TO": 2,
        }

        players_stats_map = {}
        players_stats_map["playerA"] = {
            "position": "PG",
            "FGM": 0,
            "FGA": 1,
            "FTM": 0,
            "FTA": 1,
            "TO": 5,
            "PTS": 0,
            "On IR": "False",
        }
        players_stats_map["playerB"] = {
            "position": "PG",
            "FGM": 1,
            "FGA": 2,
            "FTM": 2,
            "FTA": 1,
            "TO": 2,
            "PTS": 3,
            "On IR": "False",
        }
        players_stats_map["playerC"] = {
            "position": "C",
            "FGM": 2,
            "FGA": 2,
            "FTM": 2,
            "FTA": 2,
            "TO": 1,
            "PTS": 6,
            "On IR": "False",
        }
        players_stats_map["playerD"] = {
            "position": "PG",
            "FGM": 1,
            "FGA": 1,
            "FTM": 0,
            "FTA": 1,
            "TO": 5,
            "PTS": 0,
            "On IR": "False",
        }

        # act
        with self.assertLogs(calculations.logger, level='INFO') as captured_logs:
            compare_waiver_moves(teams, players_stats_map)

        # assert
        self.assertEqual(
            captured_logs.output,
            [
                'INFO:src.calculations:',
                'INFO:src.calculations:potential moves:',
                'INFO:src.calculations:1 win(s): drop playerA add playerD',
            ]
        )

    def test_determine_worst_player(self):
        # arrange

        # reduce stats to simplify test:
        calculations.ALL_STATS = ["FGM", "FGA", "FTM", "FTA", "TO", "PTS"]
        calculations.NINE_CATEGORIES = ["FG%", "FT%", "TO", "PTS"]

        calculations.MY_TEAM = "teamA"
        teams = {}
        teams["teamA"] = {}
        teams["teamA"]["schedule"] = ["teamB"]
        teams["teamA"]["roster"] = ["playerA", "playerB", "playerE", "playerG", "playerH"]
        teams["teamA"]["stats"] = {
            "FG%": 0.25,
            "FT%": 0.25,
            "PTS": 6,
            "TO": 6,
        }

        teams["teamB"] = {}
        teams["teamB"]["schedule"] = ["teamA"]
        teams["teamB"]["roster"] = ["playerC", "playerD", "playerF"]
        teams["teamB"]["stats"] = {
            "FG%": 0.5,
            "FT%": 0.5,
            "PTS": 24,
            "TO": 8,
        }

        players_stats_map = {}
        players_stats_map["playerA"] = {
            "FGM": 1,
            "FGA": 4,
            "FTA": 1,
            "FTM": 4,
            "TO": 3,
            "PTS": 3,
            "On IR": "False",
        }
        players_stats_map["playerB"] = {
            "FGM": 1,
            "FGA": 4,
            "FTA": 1,
            "FTM": 4,
            "TO": 4,
            "PTS": 3,
            "On IR": "False",
        }
        players_stats_map["playerC"] = {
            "FGM": 4,
            "FGA": 8,
            "FTA": 4,
            "FTM": 8,
            "TO": 4,
            "PTS": 12,
            "On IR": "False",
        }
        players_stats_map["playerD"] = {
            "FGM": 4,
            "FGA": 8,
            "FTA": 4,
            "FTM": 8,
            "TO": 4,
            "PTS": 12,
            "On IR": "False",
        }
        players_stats_map["playerE"] = {
            "FGM": 10,
            "FGA": 10,
            "FTA": 10,
            "FTM": 10,
            "TO": 0,
            "PTS": 30,
            "On IR": "False",
        }
        players_stats_map["playerF"] = {
            "FGM": 0,
            "FGA": 5,
            "FTA": 0,
            "FTM": 10,
            "TO": 10,
            "PTS": 0,
            "On IR": "False",
        }
        players_stats_map["playerG"] = {
            "FGM": 0,
            "FGA": 5,
            "FTA": 0,
            "FTM": 10,
            "TO": 10,
            "PTS": 0,
            "On IR": "True",
        }
        players_stats_map["playerH"] = {
            "FGM": 0,
            "FGA": 5,
            "FTA": 0,
            "FTM": 10,
            "TO": 10,
            "PTS": 0,
            "On IR": True,
        }

        # act
        with self.assertLogs(calculations.logger, level='INFO') as captured_logs:
            determine_worst_player(teams, players_stats_map)

        # assert
        self.assertEqual(
            captured_logs.output,
            [
                'INFO:src.calculations:',
                'INFO:src.calculations:worst players:',
                'INFO:src.calculations:0 win(s) after dropping playerA',
                'INFO:src.calculations:0 win(s) after dropping playerB',
                'INFO:src.calculations:-1 win(s) after dropping playerE',
            ]
        )

    def test_count_team_positions(self):
        # arrange
        teams = {
            "team1": {"roster": ["p1", "p2", "p3", "p4", "p5", "p6", "p7"]},
            "team2": {},
        }

        all_players_stats = {
            "p1": {"position": "PG"},
            "p2": {"position": "PG"},
            "p3": {"position": "SG"},
            "p4": {"position": "PF"},
            "p5": {"position": "C"},
            "p6": {"position": "C"},
            "p7": {"position": "C"},
        }

        # act
        count_team_positions("team1", teams, all_players_stats)

        # assert
        self.assertEqual(2, teams["team1"]["position"]["PG"])
        self.assertEqual(1, teams["team1"]["position"]["SG"])
        self.assertEqual(1, teams["team1"]["position"]["PF"])
        self.assertEqual(3, teams["team1"]["position"]["C"])

    def test_get_primary_position(self):
        # act & assert
        self.assertEqual("PG", get_primary_position("PG"))
        self.assertEqual("PG", get_primary_position("PG/SG"))
        self.assertEqual("SG", get_primary_position("SG"))
        self.assertEqual("SG", get_primary_position("SG/SF"))
        self.assertEqual("SF", get_primary_position("SF"))
        self.assertEqual("SF", get_primary_position("SF/PF"))
        self.assertEqual("SF", get_primary_position("SF/PF/C"))
        self.assertEqual("PF", get_primary_position("PF"))
        self.assertEqual("PF", get_primary_position("PF/C"))
        self.assertEqual("C", get_primary_position("C"))
