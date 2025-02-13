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


# example usage: add('Luke Kennard', 'Big Baller Brand (BBb)', all_players, teams)
def add(player, team, all_players, teams):
    if player not in all_players:
        logger.warning("unable to add {} - player not found".format(player))
    elif team not in teams:
        logger.warning("unable to add to {} - team not found".format(team))
    else:
        teams[team][KEY_ROSTER] += [player]
