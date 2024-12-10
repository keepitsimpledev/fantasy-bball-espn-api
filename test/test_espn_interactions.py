from src.espn_interactions.basketball import (
    build_teamname_to_roster_map,
    format_team_name,
)
from test.classes_for_tests import LeagueWithTeamNamesAndRosters, Team
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
        player_count = 0
        league = LeagueWithTeamNamesAndRosters()
        for team in league.teams:
            for player in team.roster:
                player_count += 1
                player.name = "player" + str(player_count)
        name_to_roster_map = build_teamname_to_roster_map(league)
        self.assertEqual(name_to_roster_map["teamA"], ["player1", "player2", "player3"])
        self.assertEqual(name_to_roster_map["teamB"], ["player4", "player5", "player6"])
        self.assertEqual(name_to_roster_map["teamC"], ["player7", "player8", "player9"])
        self.assertEqual(name_to_roster_map["teamD"], ["player10", "player11", "player12"])
