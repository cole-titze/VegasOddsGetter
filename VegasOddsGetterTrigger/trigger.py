import datetime
import logging
import VegasOddsGetter.vegas_odds_getter as odds_getter
import DataAccess.data_access as da
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    trigger()


def trigger():
    games = da.get_predicted_games()
    games = odds_getter.get_odds(games)
    da.store_probabilities(games)
