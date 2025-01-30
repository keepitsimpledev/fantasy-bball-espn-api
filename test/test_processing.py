from src.constants import KEY_ROSTER, KEY_SCHEDULE
from src.processing import (
    combine_rosters_and_schedules,
    construct_sorted_teams_stats_map,
    print_my_team_stats,
)
import src.processing as processing
from io import StringIO
from unittest.mock import patch

import unittest


class TestProcessing(unittest.TestCase):
    def test_combine_rosters_and_schedules(self):
        # arrange
        team0 = "team0 (T0)"
        team1 = "team1 (T1)"
        team2 = "team2 (T2)"

        rosters = {}
        rosters[team0] = ["player00", "player01", "player02"]
        rosters[team1] = ["player10", "player11", "player12"]
        rosters[team2] = ["player20", "player21", "player22"]

        schedules = {}
        schedules[team0] = [team1, team2]
        schedules[team1] = [team0, team2]
        schedules[team2] = [team0, team1]

        # act
        teams = combine_rosters_and_schedules(rosters, schedules)

        # assert
        self.assertEqual(teams[team0][KEY_ROSTER], ["player00", "player01", "player02"])
        self.assertEqual(teams[team1][KEY_ROSTER], ["player10", "player11", "player12"])
        self.assertEqual(teams[team2][KEY_ROSTER], ["player20", "player21", "player22"])

        self.assertEqual(teams[team0][KEY_SCHEDULE], [team1, team2])
        self.assertEqual(teams[team1][KEY_SCHEDULE], [team0, team2])
        self.assertEqual(teams[team2][KEY_SCHEDULE], [team0, team1])

    def test_construct_sorted_teams_stats_map(self):
        # arrange
        # reduce number of cats to simplify test:
        processing.NINE_CATEGORIES = [
            "REB",
            "AST",
            "PTS",
        ]
        teamA = {"stats": {"REB": 7, "AST": 5, "PTS": 3}}
        teamB = {"stats": {"REB": 5, "AST": 8, "PTS": 2}}
        teamC = {"stats": {"REB": 6, "AST": 5, "PTS": 9}}
        teams = {
            "teamA": teamA,
            "teamB": teamB,
            "teamC": teamC,
        }

        # act
        sorted_team_stats = construct_sorted_teams_stats_map(teams)

        # assert
        self.assertEqual(
            sorted_team_stats["REB"], [[7, "teamA"], [6, "teamC"], [5, "teamB"]]
        )
        self.assertEqual(
            sorted_team_stats["AST"], [[8, "teamB"], [5, "teamA"], [5, "teamC"]]
        )
        self.assertEqual(
            sorted_team_stats["PTS"], [[9, "teamC"], [3, "teamA"], [2, "teamB"]]
        )

    def test_print_my_team_stats(self):
        # arrange
        # reduce number of cats to simplify test:
        processing.NINE_CATEGORIES = ["REB", "AST", "PTS"]
        processing.MY_TEAM = "teamB"
        teamA = {"stats": {"REB": 7, "AST": 5, "PTS": 3}}
        teamB = {"stats": {"REB": 5, "AST": 8, "PTS": 2}}
        teamC = {"stats": {"REB": 6, "AST": 5, "PTS": 9}}
        teams = {
            "teamA": teamA,
            "teamB": teamB,
            "teamC": teamC,
        }

        with patch("sys.stdout", new=StringIO()) as captured_out:
            # act
            print_my_team_stats(teams)

            # assert
            self.assertEqual(
                captured_out.getvalue(),
                "teamB stat rankings:\n" + "REB : 3\nAST : 1\nPTS : 3\n",
            )
