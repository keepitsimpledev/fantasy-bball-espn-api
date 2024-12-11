from src.espn_interactions.basketball import (
    build_teamname_to_roster_map,
    format_team_name,
)
from test.classes_for_tests import LeagueWithTeamNamesAndRosters, Team
import unittest


class TestBasketball(unittest.TestCase):
    def test_format_team_name(self):
        # arrange
        team = Team("The Basketballers", "")
        # act
        result = format_team_name(team)
        # assert
        self.assertEqual("The Basketballers", result)

        # arrange
        team = Team("The Basketballers", "TB")
        # act
        formatted_name = format_team_name(team)
        # assert
        self.assertEqual("The Basketballers (TB)", formatted_name)

        # arrange
        team = Team("The⭐Basketballers", "TB")
        # act
        formatted_name = format_team_name(team)
        # assert
        self.assertEqual("TheBasketballers (TB)", formatted_name)

        # arrange
        team = Team("Who's a good boy?", "WHO")
        # act
        formatted_name = format_team_name(team)
        # assert
        self.assertEqual("Who's a good boy (WHO)", formatted_name)

    def test_build_teamname_to_roster_map(self):
        # arrange
        player_count = 0
        league = LeagueWithTeamNamesAndRosters()
        for team in league.teams:
            for player in team.roster:
                player_count += 1
                player.name = "player" + str(player_count)

        # act
        name_to_roster_map = build_teamname_to_roster_map(league)

        # assert
        self.assertEqual(name_to_roster_map["teamA"], ["player1", "player2", "player3"])
        self.assertEqual(name_to_roster_map["teamB"], ["player4", "player5", "player6"])
        self.assertEqual(name_to_roster_map["teamC"], ["player7", "player8", "player9"])
        self.assertEqual(
            name_to_roster_map["teamD"], ["player10", "player11", "player12"]
        )
