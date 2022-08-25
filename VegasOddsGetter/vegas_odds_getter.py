from pysbr import *
from datetime import timedelta
from Entities.predicted_game import PredictedGame
import logging
import Entities.vegas_enums as vegas
OddsEnum = vegas.OddsType
nhl = NHL()
sb = Sportsbook()

def get_away_team_id(away_team_abbreviation: str):
    if away_team_abbreviation == "SEA":
        return 524565
    try:
        away_team_id = nhl.team_id(away_team_abbreviation)
    except ValueError:
        away_team = away_team_abbreviation[0:2]
        away_team_id = nhl.team_id(away_team)
    return away_team_id

def get_home_team_id(home_team_abbreviation: str):
    if home_team_abbreviation == "SEA":
        return 524565
    try:
        home_team_id = nhl.team_id(home_team_abbreviation)
    except ValueError:
        home_team = home_team_abbreviation[0:2]
        home_team_id = nhl.team_id(home_team)
    return home_team_id

def make_odds_api_call(event, odds: vegas.OddsType, sports_book: vegas.SportsBook):
    if odds == OddsEnum.CLOSING:
        return CurrentLines(event['event id'], nhl.market_ids(['moneyline']), sb.id(sports_book.value))
    elif odds == OddsEnum.OPENING:
        return OpeningLines(event['event id'], nhl.market_ids(['moneyline']), sb.id(sports_book.value))

def get_odds(game: PredictedGame, sports_book: vegas.SportsBook, odds: vegas.OddsType):
    start_date = game.gameDate - timedelta(hours=13)
    end_date = game.gameDate
    home_team_id = get_home_team_id(game.homeTeamAbbreviation)
    away_team_id = get_away_team_id(game.awayTeamAbbreviation)

    # Get events and lines for events
    logging.info("Home team id: " + str(home_team_id))
    logging.info("Start Date: " + str(start_date))
    logging.info("End Date: " + str(end_date))
    logging.info("League id: " + str(nhl.league_id))

    e = EventsByParticipants([home_team_id], start_date, end_date, nhl.league_id)
    logging.info("Made it here!")
    logging.info("Number of events: " + str(len(e.ids())))
    event = e.list()[0]
    lines = make_odds_api_call(event, odds, sports_book)
    lines = lines.list(e)[:2]
    # Update vegas odds
    for line in lines:
        if line['participant id'] == home_team_id:
            game.vegasHomeOdds = line['decimal odds']
        if line['participant id'] == away_team_id:
            game.vegasAwayOdds = line['decimal odds']
    # Make sure odds aren't 0
    # Check twice to catch if only one team was incorrect
    if game.vegasHomeOdds == 0:
        game.vegasHomeOdds = -1
    if game.vegasAwayOdds == 0:
        game.vegasAwayOdds = -1
    return game
