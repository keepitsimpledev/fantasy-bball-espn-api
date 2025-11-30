from src.hashtag import get_stats, percent_to_made_and_total
import src.hashtag as hashtag

import unittest


class TestTransactions(unittest.TestCase):

    def test_percent_to_made_and_total(self):
        # act
        [fgm, fga] = percent_to_made_and_total("0.624 (9.9/15.9)")

        # assert
        self.assertEqual(fgm, 9.9)
        self.assertEqual(fga, 15.9)

    def test_get_stats(self):
        # arrange
        hashtag.HASHTAG_STATS_FILE = "test/hashtagbasketball/stats.csv"

        # act
        all_players_stats_map = get_stats()

        # assert
        jokic = {
            "position": "C",
            "FGM": 11.2,
            "FGA": 19.6,
            "FTM": 5.1,
            "FTA": 6.3,
            "3PM": 1.8,
            "REB": 13.2,
            "AST": 10.1,
            "STL": 1.9,
            "BLK": 0.7,
            "PTS": 29.3,
            "TO": 3.0,
        }
        shai = {
            "position": "PG,SG",
            "FGM": 11.0,
            "FGA": 20.5,
            "FTM": 7.0,
            "FTA": 7.9,
            "3PM": 1.6,
            "REB": 4.9,
            "AST": 6.1,
            "STL": 2.2,
            "BLK": 1.0,
            "PTS": 30.6,
            "TO": 2.8,
        }
        harden = {
            "position": "PG,SG",
            "FGM": 6.5,
            "FGA": 16.0,
            "FTM": 6.9,
            "FTA": 7.8,
            "3PM": 2.5,
            "REB": 6.0,
            "AST": 8.0,
            "STL": 1.2,
            "BLK": 0.7,
            "PTS": 22.4,
            "TO": 3.9,
        }
        maxey = {
            "position": "PG,SG",
            "FGM": 9.5,
            "FGA": 21.0,
            "FTM": 5.1,
            "FTA": 6.0,
            "3PM": 3.3,
            "REB": 3.5,
            "AST": 5.7,
            "STL": 1.6,
            "BLK": 0.3,
            "PTS": 27.4,
            "TO": 1.6,
        }

        self.assertEqual(len(all_players_stats_map), 4)
        self.assertEqual(all_players_stats_map["Nikola Jokic"], jokic)
        self.assertEqual(all_players_stats_map["Shai Gilgeous-Alexander"], shai)
        self.assertEqual(all_players_stats_map["James Harden"], harden)
        self.assertEqual(all_players_stats_map["Tyrese Maxey"], maxey)
