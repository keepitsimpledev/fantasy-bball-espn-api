from src.constants import KEY_ROSTER
import logging


logger = logging.getLogger(__name__)


# example usage: drop('Daniel Theis', teams)
def drop(player, teams):
    for team_name in teams:
        roster = teams[team_name][KEY_ROSTER]
        if player in roster:
            del roster[roster.index(player)]
            return team_name
    logger.warning("unable to drop {} - not found".format(player))
    return None
