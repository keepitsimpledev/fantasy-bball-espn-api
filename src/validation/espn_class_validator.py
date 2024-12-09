from espn_api.basketball import League


# in this validator, we confirm the structure of retrieved ESPN data,
# on which successful execution is dependent.
# these tests should identify if a future ESPN API update ruins existing logic.

def validate_league(league: League):
    if league is None:
        raise EspnClassStructureError("ESPN League object unexpectedly empty")
    raise_if_attribute_is_missing("ESPN League", league, "teams")

    if not isinstance(league.teams, list):
        raise EspnClassStructureError("ESPN League's `teams` attribute is, unexpectedly, not an array")
    if len(league.teams) < 1:
        raise EspnClassStructureError("ESPN League's `teams` attribute exists but is, unexpectedly, empty")


def raise_if_attribute_is_missing(object_name: str, object, attribute):
    if object is None or not hasattr(object, "teams"):
        raise EspnClassStructureError(
            object_name + " object missing required attribute: " + attribute
        )


class EspnClassStructureError(Exception):
    def __init__(self, message):
        super(EspnClassStructureError, self).__init__(message)
        self.message = message
