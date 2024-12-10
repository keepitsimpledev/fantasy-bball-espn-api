from espn_api.basketball import League, Team
import logging

logger = logging.getLogger(__name__)


# in this validator, we confirm the structure of retrieved ESPN data,
# on which successful execution is dependent.
# these tests should identify if a future ESPN API update ruins existing logic.


def validate_league(league: League):
    if league is None:
        raise EspnClassStructureError("ESPN League object unexpectedly empty")
    validate_league_structure(league)
    validate_teams_structure(league.teams)


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


def validate_teams_structure(teams: list[Team]):
    for team in teams:
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
