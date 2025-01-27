import src.calculations as calculations
from src.calculations import calculate_team_stats, simulate_season

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
            "On IR": "False"
        }
        players_stats_map["playerB"] = {
            "FGM": 4,
            "FGA": 10,
            "FTM": 7,
            "FTA": 8,
            "REB": 2,
            "TO": 4,
            "PTS": 17,
            "On IR": "False"
        }
        players_stats_map["playerC"] = {
            "FGM": 3,
            "FGA": 4,
            "FTM": 6,
            "FTA": 12,
            "REB": 10,
            "TO": 3,
            "PTS": 12,
            "On IR": "False"
        }
        players_stats_map["playerD"] = {
            "FGM": 12,
            "FGA": 30,
            "FTM": 11,
            "FTA": 13,
            "REB": 3,
            "TO": 5,
            "PTS": 42,
            "On IR": "True"
        }

        # act
        with self.assertLogs("src.calculations", level="WARNING") as cm:
            calculate_team_stats(teams, players_stats_map)

        # assert
        self.assertEqual(teams["teamA"]["stats"]["FG%"], .4706)
        self.assertEqual(teams["teamA"]["stats"]["FT%"], .6667)
        self.assertEqual(teams["teamA"]["stats"]["REB"], 8)
        self.assertEqual(teams["teamA"]["stats"]["TO"], -6)
        self.assertEqual(teams["teamA"]["stats"]["PTS"], 44)

        self.assertEqual(teams["teamB"]["stats"]["FG%"], .7500)
        self.assertEqual(teams["teamB"]["stats"]["FT%"], .5000)
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
