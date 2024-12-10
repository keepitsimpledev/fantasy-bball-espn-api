from src.validation.espn_class_validator import EspnClassStructureError, validate_league
import classes_for_tests
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
            validate_league(classes_for_tests.LeaguewithTeamsObject())
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League's `teams` attribute is, unexpectedly, not an array",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            validate_league(classes_for_tests.LeagueWithNoTeams())
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League's `teams` attribute is, unexpectedly, empty",
        )

    def test_validate_teams(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            validate_league(classes_for_tests.LeagueWithTeamsArray())
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Team object missing required attribute: team_name",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            validate_league(classes_for_tests.LeagueWithTeamNames())
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Team object missing required attribute: roster",
        )

        with self.assertRaises(EspnClassStructureError) as contextManager:
            validate_league(classes_for_tests.LeagueWithTeamNamesAndEmptyRosters())
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Team Basketballers's roster object is unexpectedly empty",
        )

        with self.assertLogs("src.validation.espn_class_validator", level="INFO") as cm:
            validate_league(classes_for_tests.LeagueWithTeamNamesAndRosters())
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
