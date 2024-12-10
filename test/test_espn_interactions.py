from src.espn_interactions.basketball import format_team_name
import unittest


class TestBasketball(unittest.TestCase):
    def test_format_team_name(self):
        self.assertEqual("The Basketballers", format_team_name(Team("The Basketballers", "")))
        self.assertEqual("The Basketballers (TB)", format_team_name(Team("The Basketballers", "TB")))
        self.assertEqual("TheBasketballers (TB)", format_team_name(Team("The⭐Basketballers", "TB")))
        self.assertEqual("Who's a good boy (WHO)", format_team_name(Team("Who's a good boy?", "WHO")))

class Team():
    def __init__(self, name: str, abbrev: str):
        self.team_name = name
        self.team_abbrev = abbrev
