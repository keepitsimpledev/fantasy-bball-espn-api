from src.constants import KEY_ROSTER
from src.transactions import add, drop

import unittest


class TestTransactions(unittest.TestCase):

    team0 = "team0 (T0)"
    team1 = "team1 (T1)"
    team2 = "team2 (T2)"
    all_players = [
        "player00",
        "player01",
        "player02",
        "player10",
        "player11",
        "player12",
        "player20",
        "player21",
        "player22",
        "player23",
    ]

    def setUp(self):
        # arrange
        self.team0roster = ["player00", "player01", "player02"]
        self.team1roster = ["player10", "player11", "player12"]
        self.team2roster = ["player20", "player21", "player22"]
        self.teams = {
            self.team0: {KEY_ROSTER: self.team0roster},
            self.team1: {KEY_ROSTER: self.team1roster},
            self.team2: {KEY_ROSTER: self.team2roster},
        }

    def test_drop_success(self):
        # act
        team_name = drop("player11", self.teams)

        # assert
        self.assertEqual(team_name, self.team1)
        self.assertEqual(
            self.teams[self.team0][KEY_ROSTER], ["player00", "player01", "player02"]
        )
        self.assertEqual(self.teams[self.team1][KEY_ROSTER], ["player10", "player12"])
        self.assertEqual(
            self.teams[self.team2][KEY_ROSTER], ["player20", "player21", "player22"]
        )

    def test_drop_fail(self):
        # act
        with self.assertLogs("src.transactions", level="WARNING") as cm:
            team_name = drop("player33", self.teams)

        # assert
        self.assertEqual(team_name, None)
        self.assertEqual(
            self.teams[self.team0][KEY_ROSTER], ["player00", "player01", "player02"]
        )
        self.assertEqual(
            self.teams[self.team1][KEY_ROSTER], ["player10", "player11", "player12"]
        )
        self.assertEqual(
            self.teams[self.team2][KEY_ROSTER], ["player20", "player21", "player22"]
        )
        self.assertEqual(
            cm.output[0],
            "WARNING:src.transactions:unable to drop player33 - not found",
        )

    def test_add(self):
        # act
        add("player23", self.team2, self.all_players, self.teams)

        # assert
        self.assertEqual(
            self.teams[self.team0][KEY_ROSTER], ["player00", "player01", "player02"]
        )
        self.assertEqual(
            self.teams[self.team1][KEY_ROSTER], ["player10", "player11", "player12"]
        )
        self.assertEqual(
            self.teams[self.team2][KEY_ROSTER],
            ["player20", "player21", "player22", "player23"],
        )

    def test_add_fail_player_not_found(self):
        # act
        with self.assertLogs("src.transactions", level="WARNING") as cm:
            add("player03", self.team0, self.all_players, self.teams)

        # assert
        self.assertEqual(
            self.teams[self.team0][KEY_ROSTER], ["player00", "player01", "player02"]
        )
        self.assertEqual(
            self.teams[self.team1][KEY_ROSTER], ["player10", "player11", "player12"]
        )
        self.assertEqual(
            self.teams[self.team2][KEY_ROSTER], ["player20", "player21", "player22"]
        )
        self.assertEqual(
            cm.output[0],
            "WARNING:src.transactions:unable to add player03 - player not found",
        )

    def test_add_fail_team_not_found(self):
        # act
        with self.assertLogs("src.transactions", level="WARNING") as cm:
            add("player23", "team3 (T3)", self.all_players, self.teams)

        # assert
        self.assertEqual(
            self.teams[self.team0][KEY_ROSTER], ["player00", "player01", "player02"]
        )
        self.assertEqual(
            self.teams[self.team1][KEY_ROSTER], ["player10", "player11", "player12"]
        )
        self.assertEqual(
            self.teams[self.team2][KEY_ROSTER], ["player20", "player21", "player22"]
        )
        self.assertEqual(
            cm.output[0],
            "WARNING:src.transactions:unable to add to team3 (T3) - team not found",
        )
