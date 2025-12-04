import os
import shutil
import src.processing as processing
from src.constants import KEY_ROSTER, KEY_SCHEDULE, NINE_CATEGORIES
from src.env import ESPN_LEAGUE_ID
from src.processing import (
    combine_rosters_and_schedules,
    construct_sorted_teams_stats_map,
    print_all_team_stats,
    print_my_team_stat_rankings,
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
        processing.NINE_CATEGORIES = NINE_CATEGORIES
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

        # act
        with self.assertLogs(processing.logger, level='INFO') as captured_logs:
            print_my_team_stat_rankings(teams)

        # assert
        self.assertEqual(
            captured_logs.output,
            [
                'INFO:src.processing:',
                'INFO:src.processing:teamB stat rankings:',
                'INFO:src.processing:REB : 3',
                'INFO:src.processing:AST : 1',
                'INFO:src.processing:PTS : 3',
            ]
        )

    def test_print_all_team_stats(self):
        # arrange
        processing.NINE_CATEGORIES = [
            "REB",
            "AST",
            "PTS",
        ]  # reduce number of cats to simplify test
        processing.MY_TEAM = "teamB"
        teamA = {
            "stats": {
                "FG%": 0.56789,
                "FT%": 0.72678,
                "3PM": 0.00,
                "REB": 7.00,
                "AST": 5.00,
                "BLK": 6.66,
                "STL": 5.67,
                "TO": 1.99,
                "PTS": 3.00,
            },
            "wins": 10,
            "losses": 6,
            "ties": 2,
        }
        teamB = {
            "stats": {
                "FG%": 0.456,
                "FT%": 0.891,
                "3PM": 12.55,
                "REB": 5.00,
                "AST": 8.00,
                "BLK": 0.00,
                "STL": 8.90,
                "TO": 7.65,
                "PTS": 2.00,
            },
            "wins": 8,
            "losses": 10,
            "ties": 0,
        }
        teamC = {
            "stats": {
                "FG%": 0.5001,
                "FT%": 0.7575,
                "3PM": 9.99,
                "REB": 6.00,
                "AST": 5.00,
                "BLK": 2.55,
                "STL": 4.41,
                "TO": 4.56,
                "PTS": 9.00,
            },
            "wins": 9,
            "losses": 9,
            "ties": 1,
        }
        teams = {
            "teamA": teamA,
            "teamB": teamB,
            "teamC": teamC,
        }

        # act
        with self.assertLogs(processing.logger, level='INFO') as captured_logs:
            print_all_team_stats(teams)

        # assert
        self.maxDiff = None
        self.assertEqual(
            captured_logs.output,
            [
                'INFO:src.processing:',
                'INFO:src.processing:Team  FG%    FT%    3PM    REB    AST    STL    BLK    TO     PTS    Wins',
                'INFO:src.processing:teamA 0.5679 0.7268 0.0    7.0    5.0    5.7    6.7    2.0    3.0    10',
                'INFO:src.processing:teamC 0.5001 0.7575 10.0   6.0    5.0    4.4    2.5    4.6    9.0    9',
                'INFO:src.processing:teamB 0.456  0.891  12.6   5.0    8.0    8.9    0.0    7.7    2.0    8',
            ]
        )

    def test_save_projection_to_file(self):
        # arrange
        processing.RESULTS_DIRECTORY = "test/results"

        # act
        save_projection_to_file(sample_teams())

        # assert
        with open(
            "test/results/2026 - {} projection.csv".format(ESPN_LEAGUE_ID),
            "r",
            newline="\r\n",
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
            "test/results/2026 - {} projection.csv".format(ESPN_LEAGUE_ID),
            "r",
            newline="\r\n",
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
