class TestLeague:
    def __init__(self):
        self.teams = []

    def free_agents(self, size: int):
        free_agents = []
        free_agents.append(TestPlayer("freeAgent1"))
        free_agents.append(TestPlayer("freeAgent2"))
        return free_agents


class TestTeam:
    def __init__(self):
        self.team_name = None
        self.team_abbrev = None
        self.roster = []


class TestPlayer:
    def __init__(self, player_name: str):
        self.name = player_name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)


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
