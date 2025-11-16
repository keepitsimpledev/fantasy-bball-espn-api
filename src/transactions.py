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


def find_team_of_player(player, teams):
    for team in teams:
        for team_member in teams[team][KEY_ROSTER]:
            if player == team_member:
                return team
    logger.warning("player not found or team not found for player: " + player)
    return None


def get_team_of_players(players, teams):
    team_name = find_team_of_player(players[0], teams)
    if team_name is None:
        return None

    for i in range(1, len(players)):
        if team_name != find_team_of_player(players[i], teams):
            return None
    return team_name


# example usage, 1-for-1 trade: trade(['Mason Plumlee'], ['Robert Covington'], teams)
# example usage, 3-for-3 trade: trade(['Mason Plumlee', 'Davis Bertans', 'Kyrie Irving'],
#                                   ['Dejounte Murray', 'Markelle Fultz', 'Robert Covington'], teams)
def trade(team_1_players, team_2_players, teams):
    team1 = get_team_of_players(team_1_players, teams)
    if team1 is None:
        logger.warning(
            "trade failed. these players are not on the same team: " + str(team_1_players)
        )
        return

    team2 = get_team_of_players(team_2_players, teams)
    if team2 is None:
        logger.warning(
            "trade failed. these players are not on the same team: " + str(team_2_players)
        )
        return

    if team1 == team2:
        logger.warning(
            "trade not processed. players are on the same team: " + str(team_1_players + team_2_players)
        )
        return

    for player in team_1_players + team_2_players:
        drop(player, teams)

    for player in team_1_players:
        teams[team2][KEY_ROSTER] += [player]
    for player in team_2_players:
        teams[team1][KEY_ROSTER] += [player]
