from espn_api.basketball import League
import logging

logger = logging.getLogger(__name__)


# in this validator, we confirm the structure of retrieved ESPN data,
# on which successful execution is dependent.
# these tests should identify if a future ESPN API update ruins existing logic.


def validate_league(league: League):
    if league is None:
        raise EspnClassStructureError("ESPN League object unexpectedly empty")
    validate_league_structure(league)
    validate_teams_structure(league)
    validate_player_structure(league)
    validate_schedules(league)


def validate_league_structure(league: League):
    raise_if_attribute_is_missing("ESPN League", league, "teams")
    if not isinstance(league.teams, list):
        raise EspnClassStructureError(
            "ESPN League's `teams` attribute is, unexpectedly, not an array"
        )
    if len(league.teams) < 1:
        raise EspnClassStructureError(
            "ESPN League's `teams` attribute is, unexpectedly, empty"
        )


def validate_teams_structure(league: League):
    for team in league.teams:
        raise_if_attribute_is_missing("ESPN Team", team, "team_name")
        raise_if_attribute_is_empty("ESPN team_name", team.team_name)
        raise_if_attribute_is_missing("ESPN Team", team, "roster")
        raise_if_attribute_is_empty(
            "ESPN Team {}'s roster".format(team.team_name), team.roster
        )
        if not hasattr(team, "team_abbrev"):
            logger.info(
                "ESPN Team {} is missing optional `team_abbrev` attribute".format(
                    team.team_name
                )
            )


def validate_player_structure(league: League):
    missing_name_count = 0
    total_player_count = 0

    for team in league.teams:
        for player in team.roster:
            if not hasattr(player, "name") or len(player.name) == 0:
                missing_name_count += 1
            total_player_count += 1

    for player in league.free_agents(size=1000):
        if not hasattr(player, "name") or len(player.name) == 0:
            missing_name_count += 1
        total_player_count += 1

    if missing_name_count == total_player_count:
        raise EspnClassStructureError(
            "player objects missing required `name` attribute"
        )
    elif missing_name_count > 0:
        logger.warning(
            "{} of {} player objects missing required `name` attribute".format(
                missing_name_count, total_player_count
            )
        )


def validate_schedules(league: League):
    for team in league.teams:
        raise_if_attribute_is_missing("ESPN team", team, "schedule")
        if not isinstance(team.schedule, list):
            raise EspnClassStructureError(
                "ESPN team's `schedule` attribute is, unexpectedly, not an array"
            )
        if len(team.schedule) < 1:
            raise EspnClassStructureError(
                "ESPN team's `schedule` attribute is, unexpectedly, empty"
            )
        for matchup in team.schedule:
            raise_if_attribute_is_missing("ESPN Matchup", matchup, "home_team")
            raise_if_attribute_is_missing("ESPN Matchup", matchup, "away_team")
            raise_if_attribute_is_missing(
                "ESPN Matchup.home_team", matchup.home_team, "team_name"
            )
            raise_if_attribute_is_missing(
                "ESPN Matchup.away_team", matchup.away_team, "team_name"
            )
            raise_if_attribute_is_missing(
                "ESPN Matchup.home_team", matchup.home_team, "team_abbrev"
            )
            raise_if_attribute_is_missing(
                "ESPN Matchup.away_team", matchup.away_team, "team_abbrev"
            )


def raise_if_attribute_is_missing(object_name: str, object, attribute: str):
    if object is None or not hasattr(object, attribute):
        raise EspnClassStructureError(
            object_name + " object missing required attribute: " + attribute
        )


def raise_if_attribute_is_empty(object_name: str, object):
    if len(object) < 1:
        raise EspnClassStructureError(object_name + " object is unexpectedly empty")


class EspnClassStructureError(Exception):
    def __init__(self, message):
        super(EspnClassStructureError, self).__init__(message)
        self.message = message
