from src.constants import KEY_ROSTER, KEY_SCHEDULE
from src.processing import combine_rosters_and_schedules

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
