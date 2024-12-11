from src.validation.espn_class_validator import EspnClassStructureError, validate_league
import test.classes_for_tests as classes_for_tests
import unittest


class TestEspnClassValidators(unittest.TestCase):

    def test_validate_league(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = None

            # act
            validate_league(league)

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

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN League object missing required attribute: teams",
            )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = classes_for_tests.LeaguewithTeamsObject()

            # act
            validate_league(league)

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN League's `teams` attribute is, unexpectedly, not an array",
            )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = classes_for_tests.LeagueWithNoTeams()

            # act
            validate_league(league)

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN League's `teams` attribute is, unexpectedly, empty",
            )

    def test_validate_teams(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = classes_for_tests.LeagueWithTeamsArray()

            # act
            validate_league(league)

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN Team object missing required attribute: team_name",
            )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = classes_for_tests.LeagueWithTeamNames()

            # act
            validate_league(league)

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN Team object missing required attribute: roster",
            )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = classes_for_tests.LeagueWithTeamNamesAndEmptyRosters()

            # act
            validate_league(league)

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN Team Basketballers's roster object is unexpectedly empty",
            )

        with self.assertLogs("src.validation.espn_class_validator", level="INFO") as cm:
            # arrange
            league = classes_for_tests.LeagueWithTeamNamesAndRosters()

            # act
            validate_league(league)

            # assert
            message = "INFO:src.validation.espn_class_validator:ESPN Team {} is missing optional `team_abbrev` attribute"
            self.assertEqual(
                cm.output,
                [
                    message.format("teamA"),
                    message.format("teamB"),
                    message.format("teamC"),
                    message.format("teamD"),
                ],
            )
