import os
import shutil
import src.processing as processing
from io import StringIO
from unittest.mock import patch
from src.constants import KEY_ROSTER, KEY_SCHEDULE
from src.processing import (
    combine_rosters_and_schedules,
    construct_sorted_teams_stats_map,
    print_my_team_stats,
    save_projection_to_file,
)

import unittest


def sample_teams():
    teamAStats = {
        "FG%": 0.5,
        "FT%": 0.8,
        "3PM": 100,
        "REB": 100,
        "AST": 100,
        "STL": 15,
        "BLK": 15,
        "TO": 25,
        "PTS": 200,
    }
    teamBStats = {
        "FG%": 0.6,
        "FT%": 0.7,
        "3PM": 80,
        "REB": 120,
        "AST": 75,
        "STL": 20,
        "BLK": 25,
        "TO": 20,
        "PTS": 180,
    }
    return {
        "teamA (tA)": {"stats": teamAStats, "wins": 30, "losses": 50, "ties": 2},
        "teamB (tB)": {"stats": teamBStats, "wins": 50, "losses": 30, "ties": 2},
    }


class TestProcessing(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(processing.RESULTS_DIRECTORY):
            shutil.rmtree(processing.RESULTS_DIRECTORY)
        return super().tearDown()

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

    def test_save_projection_to_file(self):
        # arrange
        processing.RESULTS_DIRECTORY = "test/results"

        # act
        save_projection_to_file(sample_teams())

        # assert
        with open(
            "test/results/2026 - 917926052 projection.csv", "r", newline="\r\n"
        ) as results_file:
            self.assertEqual(
                results_file.readline(),
                "Team,FG%,FT%,3PM,REB,AST,STL,BLK,TO,PTS,wins,losses,ties\r\n",
            )
            self.assertEqual(
                results_file.readline(),
                "teamA (tA),0.5,0.8,100,100,100,15,15,25,200,30,50,2\r\n",
            )
            self.assertEqual(
                results_file.readline(),
                "teamB (tB),0.6,0.7,80,120,75,20,25,20,180,50,30,2\r\n",
            )

    def test_save_projection_to_file_WLT(self):
        # arrange
        processing.WRITE_RECORD = True
        processing.RESULTS_DIRECTORY = "test/results"

        # act
        save_projection_to_file(sample_teams())

        # assert
        with open(
            "test/results/2026 - 917926052 projection.csv", "r", newline="\r\n"
        ) as results_file:
            self.assertEqual(
                results_file.readline(),
                "Team,FG%,FT%,3PM,REB,AST,STL,BLK,TO,PTS,Record\r\n",
            )
            self.assertEqual(
                results_file.readline(),
                "teamA (tA),0.5,0.8,100,100,100,15,15,25,200,30-50-2\r\n",
            )
            self.assertEqual(
                results_file.readline(),
                "teamB (tB),0.6,0.7,80,120,75,20,25,20,180,50-30-2\r\n",
            )
