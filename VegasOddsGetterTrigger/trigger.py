import datetime
import logging
import time
import math
import VegasOddsGetter.vegas_odds_getter as odds_getter
import DataAccess.data_access as da
import azure.functions as func
import Entities.vegas_enums as vegas
SportsBooks = vegas.SportsBook
Odds = vegas.OddsType

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    trigger()

# Foreach sportsbook get the opening and closing odds for a set number of games
# Save the games after each odds for each sportsbook
def trigger():
    start = 0
    end = 0
    sports_books = [SportsBooks.BOVADA, SportsBooks.MY_BOOKIE, SportsBooks.BET_365, SportsBooks.BET_ONLINE, SportsBooks.PINNACLE]
    odds_to_find = [Odds.CLOSING, Odds.OPENING]
    for sb in sports_books:
        for odds in odds_to_find:
            sports_book = str(sb.value)
            sports_book = sports_book[0].lower() + sports_book[1:]
            column_name = sports_book + odds.value
            games = da.get_predicted_games(column_name)
            logging.info("Number of games to process: " + str(len(games)))
            for game in games:
                elapsed_time = math.floor(end - start)
                # Wait 15 seconds between calls to not rate limit api
                time.sleep(6 - elapsed_time)
                start = time.time()
                predicted_game = odds_getter.get_odds(game, sb, odds)
                da.store_probability(predicted_game, column_name)
                end = time.time()
