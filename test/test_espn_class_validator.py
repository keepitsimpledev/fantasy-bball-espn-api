from src.validation.espn_class_validator import (
    EspnClassStructureError,
    validate_league,
    validate_league_structure,
    validate_teams_structure,
    validate_player_structure,
    validate_schedules
)
from test.classes_for_tests import GetTestLeague
import unittest


class TestEspnClassValidators(unittest.TestCase):


    def test_validate_league_exists(self):
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


    def test_validate_league_has_teams(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = {}

            # act
            validate_league_structure(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League object missing required attribute: teams",
        )


    def test_validate_teams_is_list(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            league.teams = {}

            # act
            validate_league_structure(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League's `teams` attribute is, unexpectedly, not an array",
        )


    def test_validate_teams_are_found(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            league.teams = []

            # act
            validate_league_structure(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN League's `teams` attribute is, unexpectedly, empty",
        )


    def test_validate_teams_have_names(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                del team.team_name

            # act
            validate_teams_structure(league.teams)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Team object missing required attribute: team_name",
        )


    def test_validate_teams_have_rosters(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                del team.roster

            # act
            validate_teams_structure(league.teams)

            # assert
            self.assertEqual(
                contextManager.exception.message,
                "ESPN Team object missing required attribute: roster",
            )


    def test_validate_rosters_are_found(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                team.roster = []

            # act
            validate_teams_structure(league.teams)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Team team0's roster object is unexpectedly empty",
        )


    def test_check_for_team_abbrev_log(self):
        with self.assertLogs("src.validation.espn_class_validator", level="INFO") as cm:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                del team.team_abbrev

            # act
            validate_teams_structure(league.teams)

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


    def test_validate_players_have_names(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()

            for team in league.teams:
                for player in team.roster:
                    del player.name
            for player in league.free_agents(size=1000):
                del player.name

            # act
            validate_player_structure(league)
            self.fail("expected EspnClassStructureError was not raised")

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "player objects missing required `name` attribute",
        )


    def test_validate_all_players_have_names(self):
        with self.assertLogs(
            "src.validation.espn_class_validator", level="WARNING"
        ) as cm:
            # arrange
            league = GetTestLeague()
            del league.teams[0].roster[0].name
            del league.free_agents(size=1000)[0].name

            # act
            validate_player_structure(league)

            # assert
            self.assertEqual(
                cm.output[0],
                "WARNING:src.validation.espn_class_validator:2 of 11 player objects missing required `name` attribute",
            )
    

    def test_validate_team_has_schedule(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                del team.schedule

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN team object missing required attribute: schedule",
        )
        
        
    def test_validate_schedules_are_lists(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                team.schedule = {}

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN team's `schedule` attribute is, unexpectedly, not an array",
        )
        
        
    def test_validate_schedules_are_found(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                team.schedule = []

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN team's `schedule` attribute is, unexpectedly, empty",
        )
        
        
    def test_validate_home_teams_are_found(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                for schedule in team.schedule:
                    del schedule.home_team

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Matchup object missing required attribute: home_team",
        )
        
        
    def test_validate_away_teams_are_found(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                for schedule in team.schedule:
                    del schedule.away_team

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Matchup object missing required attribute: away_team",
        )
        
        
    def test_validate_home_teams_have_name(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                for matchup in team.schedule:
                    if hasattr(matchup.home_team, "team_name"):
                        del matchup.home_team.team_name

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Matchup.home_team object missing required attribute: team_name",
        )
        
        
    def test_validate_home_teams_have_abbrev(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                for matchup in team.schedule:
                    if hasattr(matchup.home_team, "team_abbrev"):
                        del matchup.home_team.team_abbrev

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Matchup.home_team object missing required attribute: team_abbrev",
        )
        

    def test_validate_away_teams_have_name(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                for matchup in team.schedule:
                    if hasattr(matchup.away_team, "team_name"):
                        del matchup.away_team.team_name

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Matchup.away_team object missing required attribute: team_name",
        )
        

    def test_validate_away_teams_have_abbrev(self):
        with self.assertRaises(EspnClassStructureError) as contextManager:
            # arrange
            league = GetTestLeague()
            for team in league.teams:
                for matchup in team.schedule:
                    if hasattr(matchup.away_team, "team_abbrev"):
                        del matchup.away_team.team_abbrev

            # act
            validate_schedules(league)

        # assert
        self.assertEqual(
            contextManager.exception.message,
            "ESPN Matchup.away_team object missing required attribute: team_abbrev",
        )
