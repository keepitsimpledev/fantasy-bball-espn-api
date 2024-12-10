class LeaguewithTeamsObject:
    teams = {}


class LeagueWithNoTeams:
    teams = []


class LeagueWithTeamsArray:
    teams = [{}, {}, {}, {}]


class TeamWithAName:
    team_name = "a name"


class TeamWithANameAndEmptyRoster:
    team_name = "Basketballers"
    roster = {}


class Player:
    name = "player name"


class TeamWithARoster:
    def __init__(self, name):
        self.team_name = name
        self.roster = {
            Player(),
            Player(),
            Player(),
        }


class LeagueWithTeamNames:
    teams = [TeamWithAName, TeamWithAName, TeamWithAName, TeamWithAName]


class LeagueWithTeamNamesAndEmptyRosters:
    teams = [
        TeamWithANameAndEmptyRoster,
        TeamWithANameAndEmptyRoster,
        TeamWithANameAndEmptyRoster,
        TeamWithANameAndEmptyRoster,
    ]


class LeagueWithTeamNamesAndRosters:
    teams = [
        TeamWithARoster("teamA"),
        TeamWithARoster("teamB"),
        TeamWithARoster("teamC"),
        TeamWithARoster("teamD"),
    ]


class Team:
    def __init__(self, name: str, abbrev: str):
        self.team_name = name
        self.team_abbrev = abbrev
