from src.constants import ALL_STATS, ESPN_STATS_KEY, ESPN_STATS_TOTAL_KEY
from src.espn_interactions.basketball import (
    build_teamname_to_roster_map,
    construct_players_stats_map,
    extract_all_players_from_league,
    extract_schedules_from_espn_league,
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

        with self.assertLogs("src.espn_interactions.basketball", level="INFO") as cm:
            # arrange
            league = GetTestLeague()

            # act
            construct_players_stats_map(league)

            # assert
            self.assertEqual(
                cm.output,
                [
                    "INFO:src.espn_interactions.basketball:player00 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player01 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player02 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player10 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player11 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player12 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player20 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player21 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:player22 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:freeAgent1 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                    "INFO:src.espn_interactions.basketball:freeAgent2 projections not found: FGM, FGA, FTM, FTA, 3PM, REB, AST, STL, BLK, TO, PTS",
                ],
            )

        # arrange
        league = GetTestLeague()

        players = []
        for team in league.teams:
            for player in team.roster:
                players.append(player)
        for player in league.free_agents(size=1000):
            players.append(player)

        expected_stat_value = 1
        for player in players:
            player.stats[ESPN_STATS_KEY] = {}
            player.stats[ESPN_STATS_KEY][ESPN_STATS_TOTAL_KEY] = {}

            for stat in ALL_STATS:
                player.stats[ESPN_STATS_KEY][ESPN_STATS_TOTAL_KEY][stat] = expected_stat_value
                expected_stat_value += 1

        # act
        stats_map = construct_players_stats_map(league)

        # assert
        expected_stat_value = 1
        for player_stats in stats_map.keys():
            for stat in ALL_STATS:
                # assertion failure messages here are not very helpful,
                # but we'll accept it for ease of assertion
                self.assertEqual(expected_stat_value, stats_map[player_stats][stat])
                expected_stat_value += 1


    def test_extract_schedules_from_espn_league(self):
        # arrange
        league = GetTestLeague()

        # act
        schedules = extract_schedules_from_espn_league(league)

        # assert
        self.assertEqual(schedules["team0 (T0)"][0], "team1 (T1)")
        self.assertEqual(schedules["team0 (T0)"][1], "team2 (T2)")
        self.assertEqual(schedules["team1 (T1)"][0], "team0 (T0)")
        self.assertEqual(schedules["team1 (T1)"][1], "team2 (T2)")
        self.assertEqual(schedules["team2 (T2)"][0], "team0 (T0)")
        self.assertEqual(schedules["team2 (T2)"][1], "team1 (T1)")
