from espn_api.basketball import League


def validate_league(league: League):
    if not hasattr(league, "team"):
        raise EspnClassStructureError(
            "ESPN League object missing required attribute: team"
        )


class EspnClassStructureError(Exception):
    def __init__(self, message):
        super(EspnClassStructureError, self).__init__(message)
        self.message = message
