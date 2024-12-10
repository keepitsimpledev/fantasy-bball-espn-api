from src.espn_interactions.basketball import build_teamname_to_roster_map, format_team_name
from classes_for_tests import LeagueWithTeamNamesAndRosters, Team
import unittest


class TestBasketball(unittest.TestCase):
    def test_format_team_name(self):
        self.assertEqual(
            "The Basketballers", format_team_name(Team("The Basketballers", ""))
        )
        self.assertEqual(
            "The Basketballers (TB)", format_team_name(Team("The Basketballers", "TB"))
        )
        self.assertEqual(
            "TheBasketballers (TB)", format_team_name(Team("The⭐Basketballers", "TB"))
        )
        self.assertEqual(
            "Who's a good boy (WHO)", format_team_name(Team("Who's a good boy?", "WHO"))
        )

    def test_build_teamname_to_roster_map(self):
        build_teamname_to_roster_map(LeagueWithTeamNamesAndRosters())
        this_has_been_sufficiently_verified = False
        self.assertTrue(this_has_been_sufficiently_verified)
