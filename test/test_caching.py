import csv
import os  # TODO: consider mocking rather than using os
import shutil
import src.caching as caching
from src.caching import cache_teams, init_cache_folders, load_teams, CachingError

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

    def test_cache_teams(self):
        # arrange
        teams = {}
        teams["teamA"] = ["p1", "p2"]
        teams["teamB"] = ["p3", "p4"]
        os.mkdir("test/cached/")
        os.mkdir("test/cached/12345/")
        os.mkdir("test/cached/12345/teams/")

        # act
        cache_teams(teams)

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

    def test_load_teams(self):
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
        teams = load_teams()

        # assert
        self.assertEqual(len(teams), 2)
        self.assertEqual(teams["teamA"][0], "p1")
        self.assertEqual(teams["teamA"][1], "p2")
        self.assertEqual(teams["teamB"][0], "p3")
        self.assertEqual(teams["teamB"][1], "p4")

    def test_load_teams_not_enough_teams(self):
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
            load_teams()
            self.fail("expected CachingError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "expected multiple team files but found 1",
        )

    def test_load_teams_not_enough_players(self):
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
            load_teams()
            self.fail("expected CachingError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "expected multiple players for team teamB but found 1",
        )
