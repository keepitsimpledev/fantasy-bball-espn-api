from src.constants import KEY_ROSTER
from src.transactions import drop

import unittest


class TestTransactions(unittest.TestCase):

    def test_drop_success(self):
        # arrange
        team0 = "team0 (T0)"
        team1 = "team1 (T1)"
        team2 = "team2 (T2)"

        teams = {
            team0: {KEY_ROSTER: ["player00", "player01", "player02"]},
            team1: {KEY_ROSTER: ["player10", "player11", "player12"]},
            team2: {KEY_ROSTER: ["player20", "player21", "player22"]},
        }

        # act
        team_name = drop("player11", teams)

        # assert
        self.assertEqual(team_name, team1)
        self.assertEqual(teams[team0][KEY_ROSTER], ["player00", "player01", "player02"])
        self.assertEqual(teams[team1][KEY_ROSTER], ["player10", "player12"])
        self.assertEqual(teams[team2][KEY_ROSTER], ["player20", "player21", "player22"])

    def test_drop_fail(self):
        # arrange
        team0 = "team0 (T0)"
        team1 = "team1 (T1)"
        team2 = "team2 (T2)"

        teams = {
            team0: {KEY_ROSTER: ["player00", "player01", "player02"]},
            team1: {KEY_ROSTER: ["player10", "player11", "player12"]},
            team2: {KEY_ROSTER: ["player20", "player21", "player22"]},
        }

        # act
        with self.assertLogs("src.transactions", level="WARNING") as cm:
            team_name = drop("player33", teams)

        # assert
        self.assertEqual(team_name, None)
        self.assertEqual(teams[team0][KEY_ROSTER], ["player00", "player01", "player02"])
        self.assertEqual(teams[team1][KEY_ROSTER], ["player10", "player11", "player12"])
        self.assertEqual(teams[team2][KEY_ROSTER], ["player20", "player21", "player22"])
        self.assertEqual(
            cm.output[0],
            "WARNING:src.transactions:unable to drop player33 - not found",
        )
