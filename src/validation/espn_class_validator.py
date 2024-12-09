from espn_api.basketball import League


def validate_league(league: League):
    if league is None:
        raise EspnClassStructureError("ESPN League object unexpectedly empty")
    raise_if_attribute_is_missing("ESPN League", league, "teams")


def raise_if_attribute_is_missing(object_name: str, object, attribute):
    if object is None or not hasattr(object, "teams"):
        raise EspnClassStructureError(
            object_name + " object missing required attribute: " + attribute
        )


class EspnClassStructureError(Exception):
    def __init__(self, message):
        super(EspnClassStructureError, self).__init__(message)
        self.message = message
