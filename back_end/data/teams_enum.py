from enum import Enum

class NBATeam(Enum):
    ATL = "Atlanta Hawks"
    BOS = "Boston Celtics"
    BKN = "Brooklyn Nets"
    CHA = "Charlotte Hornets"
    CHI = "Chicago Bulls"
    CLE = "Cleveland Cavaliers"
    DAL = "Dallas Mavericks"
    DEN = "Denver Nuggets"
    DET = "Detroit Pistons"
    GSW = "Golden State Warriors"
    HOU = "Houston Rockets"
    IND = "Indiana Pacers"
    LAC = "LA Clippers"
    LAL = "Los Angeles Lakers"
    MEM = "Memphis Grizzlies"
    MIA = "Miami Heat"
    MIL = "Milwaukee Bucks"
    MIN = "Minnesota Timberwolves"
    NOP = "New Orleans Pelicans"
    NYK = "New York Knicks"
    OKC = "Oklahoma City Thunder"
    ORL = "Orlando Magic"
    PHI = "Philadelphia 76ers"
    PHO = "Phoenix Suns"
    POR = "Portland Trail Blazers"
    SAC = "Sacramento Kings"
    SAS = "San Antonio Spurs"
    TOR = "Toronto Raptors"
    UTA = "Utah Jazz"
    WAS = "Washington Wizards"


    def get_team_abbreviation(team_name):
        for team in NBATeam:
            if team.value == team_name:
                return team.name




