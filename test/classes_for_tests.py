class TestLeague:
    def __init__(self):
        self.teams = []

        self.free_agent_players = []
        self.free_agent_players.append(TestPlayer("freeAgent1"))
        self.free_agent_players.append(TestPlayer("freeAgent2"))

    def free_agents(self, size: int):
        return self.free_agent_players


class TestTeam:
    def __init__(self):
        self.team_name = None
        self.team_abbrev = None
        self.roster = []
        self.schedule = []


class TestPlayer:
    def __init__(self, player_name: str):
        self.name = player_name
        self.stats = {}
        self.lineupSlot = None

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)


class TestMatchup:
    def __init__(self, team_a: TestTeam, team_b: TestTeam):
        self.home_team = TestTeam()
        self.home_team.team_name = team_a.team_name
        self.home_team.team_abbrev = team_a.team_abbrev

        self.away_team = TestTeam()
        self.away_team.team_name = team_b.team_name
        self.away_team.team_abbrev = team_b.team_abbrev


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

    for left_team in league.teams:
        for right_team in league.teams:
            if left_team != right_team:
                left_team.schedule.append(TestMatchup(left_team, right_team))

    return league


