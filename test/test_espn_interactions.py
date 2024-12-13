from src.espn_interactions.basketball import (
    build_teamname_to_roster_map,
    format_team_name,
)
from test.classes_for_tests import GetTestLeague, TestTeam
import unittest


class TestBasketball(unittest.TestCase):
    def test_format_team_name(self):
        # arrange
        team = TestTeam()
        team.team_name = "The Basketballers"
        team.team_abbrev = ""
        # act
        result = format_team_name(team)
        # assert
        self.assertEqual("The Basketballers", result)

        # arrange
        team = TestTeam()
        team.team_name = "The Basketballers"
        team.team_abbrev = "TB"
        # act
        formatted_name = format_team_name(team)
        # assert
        self.assertEqual("The Basketballers (TB)", formatted_name)

        # arrange
        team = TestTeam()
        team.team_name = "The⭐Basketballers"
        team.team_abbrev = "TB"
        # act
        formatted_name = format_team_name(team)
        # assert
        self.assertEqual("TheBasketballers (TB)", formatted_name)

        # arrange
        team = TestTeam()
        team.team_name = "Who's a good boy?"
        team.team_abbrev = "WHO"
        # act
        formatted_name = format_team_name(team)
        # assert
        self.assertEqual("Who's a good boy (WHO)", formatted_name)

    def test_build_teamname_to_roster_map(self):
        # arrange
        league = GetTestLeague()

        # act
        name_to_roster_map = build_teamname_to_roster_map(league)

        # assert
        self.assertEqual(
            name_to_roster_map["team0 (T0)"], ["player00", "player01", "player02"]
        )
        self.assertEqual(
            name_to_roster_map["team1 (T1)"], ["player10", "player11", "player12"]
        )
        self.assertEqual(
            name_to_roster_map["team2 (T2)"], ["player20", "player21", "player22"]
        )
