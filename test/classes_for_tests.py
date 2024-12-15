class TestLeague:
    def __init__(self):
        self.teams = []


class TestTeam:
    def __init__(self):
        self.team_name = None
        self.team_abbrev = None
        self.roster = []


class TestPlayer:
    def __init__(self, player_name: str):
        self.name = player_name


def GetTestLeague():
    league = TestLeague()

    for team_number in range(3):
        team = TestTeam()
        team.team_name = "team" + str(team_number)
        team.team_abbrev = "T" + str(team_number)
        league.teams.append(team)

        for player_number in range(3):
            player = TestPlayer("player" + str(team_number) + str(player_number))
            team.roster.append(player)

    return league
