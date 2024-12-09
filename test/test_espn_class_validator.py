from src.validation.espn_class_validator import (
    EspnClassStructureError,
    validate_league)
import unittest


class TestEspnClassValidators(unittest.TestCase):

    def test_validate_league(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            validate_league(None)
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League object unexpectedly empty",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            validate_league({})
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League object missing required attribute: teams",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            validate_league(LeaguewithTeamsObject())
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League's `teams` attribute is, unexpectedly, not an array",
        )

        validate_league(LeagueWithTeamsArray())


class LeaguewithTeamsObject:
    teams = {}


class LeagueWithTeamsArray:
    teams = []
