from dataclasses import dataclass
from datetime import datetime

@dataclass
class PredictedGame:
    id: int
    homeTeamAbbreviation: str
    awayTeamAbbreviation: str
    gameDate: datetime
    vegasHomeOdds: float
    vegasAwayOdds: float

    def get_home_odds(self):
        return 1/self.vegasHomeOdds

    def get_away_odds(self):
        return 1/self.vegasAwayOdds
