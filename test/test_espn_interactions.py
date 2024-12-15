from src.espn_interactions.basketball import (
    build_teamname_to_roster_map,
    construct_players_stats_map,
    extract_all_players_from_league,
    format_team_name,
)
from test.classes_for_tests import GetTestLeague, TestPlayer, TestTeam
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

    def test_extract_players_from_league(self):
        # arrange
        league = GetTestLeague()

        # act
        players = extract_all_players_from_league(league)

        # assert
        self.assertEqual(11, len(players))
        self.assertIn(TestPlayer("player00"), players)
        self.assertIn(TestPlayer("player01"), players)
        self.assertIn(TestPlayer("player02"), players)
        self.assertIn(TestPlayer("player10"), players)
        self.assertIn(TestPlayer("player11"), players)
        self.assertIn(TestPlayer("player12"), players)
        self.assertIn(TestPlayer("player20"), players)
        self.assertIn(TestPlayer("player21"), players)
        self.assertIn(TestPlayer("player22"), players)
        self.assertIn(TestPlayer("freeAgent1"), players)
        self.assertIn(TestPlayer("freeAgent2"), players)

    def test_construct_players_stat_map(self):
        # arrange
        league = GetTestLeague()

        # act
        players_stats_map = construct_players_stats_map(league)

        # assert
        self.assertIsNone(players_stats_map)
