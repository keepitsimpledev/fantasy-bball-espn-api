import unittest, os, shutil
import src.caching as caching
from src.caching import init_cache_folders


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
        open("test/cached/12345/teams/teams.txt", 'w').close()
        open("test/cached/12345/schedules/schedules.txt", 'w').close()

        # act
        init_cache_folders()

        # assert
        self.assertTrue(os.path.exists("test/cached/12345/"))
        self.assertTrue(os.path.exists("test/cached/12345/teams/"))
        self.assertTrue(os.path.exists("test/cached/12345/schedules/"))
