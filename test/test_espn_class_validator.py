from src.validation.espn_class_validator import EspnClassStructureError, validate_league
from test.classes_for_tests import GetTestLeague
import unittest


class TestEspnClassValidators(unittest.TestCase):

    def test_validate_league(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = None

            # act
            validate_league(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League object unexpectedly empty",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = {}

            # act
            validate_league(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League object missing required attribute: teams",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            league.teams = {}

            # act
            validate_league(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League's `teams` attribute is, unexpectedly, not an array",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            league.teams = []

            # act
            validate_league(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League's `teams` attribute is, unexpectedly, empty",
        )

    def test_validate_teams(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                del team.team_name

            # act
            validate_league(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Team object missing required attribute: team_name",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                del team.roster

            # act
            validate_league(league)

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN Team object missing required attribute: roster",
            )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                team.roster = []

            # act
            validate_league(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Team team0's roster object is unexpectedly empty",
        )

        with self.assertLogs("src.validation.espn_class_validator", level="INFO") as cm:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                del team.team_abbrev

            # act
            validate_league(league)

            # assert
            message = "INFO:src.validation.espn_class_validator:ESPN Team {} is missing optional `team_abbrev` attribute"
            self.assertEqual(
                cm.output,
                [
                    message.format("team0"),
                    message.format("team1"),
                    message.format("team2"),
                ],
            )
