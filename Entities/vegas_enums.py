from enum import Enum

class OddsType(Enum):
    OPENING = "Opening"
    CLOSING = "Closing"

class SportsBook(Enum):
    BOVADA = "Bovada"
    MY_BOOKIE = "MyBookie"
    PINNACLE = "Pinnacle"
    BET_ONLINE = "BetOnline"
    BET_365 = "Bet365"
