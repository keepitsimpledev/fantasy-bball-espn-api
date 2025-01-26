import csv
import os  # TODO: consider mocking rather than using os
import shutil
import src.caching as caching
from src.caching import (
    cache_players_stats_map,
    cache_rosters,
    cache_schedules,
    init_cache_folders,
    load_players_stats_map,
    load_rosters,
    load_schedules,
    CachingError,
)

import unittest


class TestCaching(unittest.TestCase):

    # perform filesystem tests within test directory:
    caching.CACHE_DIRECTORY = "test/" + caching.CACHE_DIRECTORY
    # don't use actual ESPN league ID during tests:
    caching.ESPN_LEAGUE_ID = 12345

    def setUp(self):
        if os.path.exists(caching.CACHE_DIRECTORY):
            shutil.rmtree(caching.CACHE_DIRECTORY)
        return super().setUp()

    def tearDown(self):
        if os.path.exists(caching.CACHE_DIRECTORY):
            shutil.rmtree(caching.CACHE_DIRECTORY)
        return super().tearDown()

    def test_init_cache_folders_from_empty(self):
        # act
        init_cache_folders()

        # assert
        self.assertTrue(os.path.exists("test/cached/12345/"))
        self.assertTrue(os.path.exists("test/cached/12345/teams/"))
        self.assertTrue(os.path.exists("test/cached/12345/schedules/"))

    def test_init_cache_folders_from_existing(self):
        # arrange
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/teams/")
        os.mkdir("test/cached/12345/schedules/")
        open("test/cached/12345/teams/teams.txt", "w").close()
        open("test/cached/12345/schedules/schedules.txt", "w").close()

        # act
        init_cache_folders()

        # assert
        self.assertTrue(os.path.exists("test/cached/12345/"))
        self.assertTrue(os.path.exists("test/cached/12345/teams/"))
        self.assertTrue(os.path.exists("test/cached/12345/schedules/"))
        self.assertFalse(os.path.exists("test/cached/12345/teams/teams.txt"))
        self.assertFalse(os.path.exists("test/cached/12345/schedules/schedules.txt"))

    def test_init_cache_folders_dont_clear_other_league(self):
        # arrange
        os.mkdir("test/cached/")
        os.mkdir("test/cached/67890/")
        os.mkdir("test/cached/67890/teams/")
        open("test/cached/67890/teams/teams.txt", "w").close()

        # act
        init_cache_folders()

        # assert
        self.assertTrue(os.path.exists("test/cached/67890/teams/teams.txt"))

    def test_cache_rosters(self):
        # arrange
        rosters = {}
        rosters["teamA"] = ["p1", "p2"]
        rosters["teamB"] = ["p3", "p4"]
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/teams/")

        # act
        cache_rosters(rosters)

        # assert
        with open(
            "test/cached/12345/teams/teamA.csv", "r", newline="\r\n"
        ) as team_file:
            self.assertEqual(team_file.readline(), "p1\r\n")
            self.assertEqual(team_file.readline(), "p2\r\n")
        with open(
            "test/cached/12345/teams/teamB.csv", "r", newline="\r\n"
        ) as team_file:
            self.assertEqual(team_file.readline(), "p3\r\n")
            self.assertEqual(team_file.readline(), "p4\r\n")

    def test_load_rosters(self):
        # arrange
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/teams/")
        with open("test/cached/12345/teams/teamA.csv", "w", newline="\n") as team_file:
            writer = csv.writer(team_file)
            writer.writerow(["p1"])
            writer.writerow(["p2"])
        with open("test/cached/12345/teams/teamB.csv", "w", newline="\n") as team_file:
            writer = csv.writer(team_file)
            writer.writerow(["p3"])
            writer.writerow(["p4"])

        # act
        rosters = load_rosters()

        # assert
        self.assertEqual(len(rosters), 2)
        self.assertEqual(rosters["teamA"][0], "p1")
        self.assertEqual(rosters["teamA"][1], "p2")
        self.assertEqual(rosters["teamB"][0], "p3")
        self.assertEqual(rosters["teamB"][1], "p4")

    def test_load_rosters_not_enough_teams(self):
        # arrange
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/teams/")
        with open("test/cached/12345/teams/teamA.csv", "w", newline="\n") as team_file:
            writer = csv.writer(team_file)
            writer.writerow(["p1"])
            writer.writerow(["p2"])

        # act
        with self.assertRaises(CachingError) as contextManager:
            load_rosters()
            self.fail("expected CachingError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "expected multiple team files but found 1",
        )

    def test_load_rosters_not_enough_players(self):
        # arrange
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/teams/")
        with open("test/cached/12345/teams/teamA.csv", "w", newline="\n") as team_file:
            writer = csv.writer(team_file)
            writer.writerow(["p1"])
            writer.writerow(["p2"])
        with open("test/cached/12345/teams/teamB.csv", "w", newline="\n") as team_file:
            writer = csv.writer(team_file)
            writer.writerow(["p3"])

        # act
        with self.assertRaises(CachingError) as contextManager:
            load_rosters()
            self.fail("expected CachingError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "expected multiple players for team teamB but found 1",
        )

    def test_cache_players_stats_map(self):
        # arrange
        caching.ALL_STATS = ["STL", "BLK"]  # to simplify test a bit
        players_stats_map = {}
        players_stats_map["TJ McConnell"] = {}
        players_stats_map["TJ McConnell"]["STL"] = 95
        players_stats_map["TJ McConnell"]["BLK"] = 14
        players_stats_map["TJ McConnell"]["On IR"] = False
        players_stats_map["Walker Kessler"] = {}
        players_stats_map["Walker Kessler"]["STL"] = 28
        players_stats_map["Walker Kessler"]["BLK"] = 192
        players_stats_map["Walker Kessler"]["On IR"] = True
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")

        # act
        cache_players_stats_map(players_stats_map)

        # assert
        with open("test/cached/12345/players.csv", "r", newline="\r\n") as team_file:
            self.assertEqual(team_file.readline(), "Player,STL,BLK,On IR\r\n")
            self.assertEqual(team_file.readline(), "TJ McConnell,95,14,False\r\n")
            self.assertEqual(team_file.readline(), "Walker Kessler,28,192,True\r\n")

    def test_load_players_stats_map(self):
        # arrange
        caching.ALL_STATS = ["STL", "BLK"]  # to simplify test a bit
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        with open("test/cached/12345/players.csv", "w", newline="\n") as players_file:
            writer = csv.writer(players_file)
            writer.writerow(["Player", "STL", "BLK", "On IR"])
            writer.writerow(["TJ McConnell", 95, 14, False])
            writer.writerow(["Walker Kessler", 28, 192, True])
            for player_num in range(200):  # enough players to not trigger the validation count
                writer.writerow(["player{}".format(player_num), 0, 0, False])

        # act
        teams = load_players_stats_map()

        # assert
        self.assertEqual(len(teams), 202)
        self.assertEqual(teams["TJ McConnell"]["STL"], 95)
        self.assertEqual(teams["TJ McConnell"]["BLK"], 14)
        self.assertEqual(teams["TJ McConnell"]["On IR"], "False")
        self.assertEqual(teams["Walker Kessler"]["STL"], 28)
        self.assertEqual(teams["Walker Kessler"]["BLK"], 192)
        self.assertEqual(teams["Walker Kessler"]["On IR"], "True")

    def test_load_players_stats_map_not_enough_players(self):
        # arrange
        caching.ALL_STATS = ["STL", "BLK"]  # to simplify test a bit
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        with open("test/cached/12345/players.csv", "w", newline="\n") as players_file:
            writer = csv.writer(players_file)
            writer.writerow(["Player", "STL", "BLK", "On IR"])
            writer.writerow(["TJ McConnell", 95, 14, False])
            writer.writerow(["Walker Kessler", 28, 192, True])

        # act
        with self.assertRaises(CachingError) as contextManager:
            load_players_stats_map()()
            self.fail("expected CachingError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "expected no less than 350 players but found 2",
        )

    def test_cache_schedules(self):
        # arrange
        schedules = {}
        schedules["teamA"] = ["teamB", "teamC"]
        schedules["teamB"] = ["teamA", "teamC"]
        schedules["teamC"] = ["teamA", "teamB"]
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/schedules/")

        # act
        cache_schedules(schedules)

        # assert
        with open(
            "test/cached/12345/schedules/teamA.csv", "r", newline="\r\n"
        ) as team_file:
            self.assertEqual(team_file.readline(), "teamB\r\n")
            self.assertEqual(team_file.readline(), "teamC\r\n")
        with open(
            "test/cached/12345/schedules/teamB.csv", "r", newline="\r\n"
        ) as team_file:
            self.assertEqual(team_file.readline(), "teamA\r\n")
            self.assertEqual(team_file.readline(), "teamC\r\n")
        with open(
            "test/cached/12345/schedules/teamC.csv", "r", newline="\r\n"
        ) as team_file:
            self.assertEqual(team_file.readline(), "teamA\r\n")
            self.assertEqual(team_file.readline(), "teamB\r\n")

    def test_load_schedules(self):
        # arrange
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/schedules/")
        with open(
            "test/cached/12345/schedules/teamA.csv", "w", newline="\n"
        ) as players_file:
            writer = csv.writer(players_file)
            writer.writerow(["teamB"])
            writer.writerow(["teamC"])
        with open(
            "test/cached/12345/schedules/teamB.csv", "w", newline="\n"
        ) as players_file:
            writer = csv.writer(players_file)
            writer.writerow(["teamA"])
            writer.writerow(["teamC"])
        with open(
            "test/cached/12345/schedules/teamC.csv", "w", newline="\n"
        ) as players_file:
            writer = csv.writer(players_file)
            writer.writerow(["teamA"])
            writer.writerow(["teamB"])

        # act
        schedules = load_schedules()

        # assert
        self.assertEqual(len(schedules), 3)
        self.assertEqual(schedules["teamA"][0], "teamB")
        self.assertEqual(schedules["teamA"][1], "teamC")
        self.assertEqual(schedules["teamB"][0], "teamA")
        self.assertEqual(schedules["teamB"][1], "teamC")
        self.assertEqual(schedules["teamC"][0], "teamA")
        self.assertEqual(schedules["teamC"][1], "teamB")
