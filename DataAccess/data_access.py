import pyodbc
import os
from Entities.Mappers import predicted_game_mapper
from Entities.predicted_game import PredictedGame

def get_server():
    return 'nhl-game.database.windows.net'
def get_database():
    return os.environ["SQL_DATABASE"]
def get_username():
    return os.environ["SQL_USERNAME"]
def get_password():
    return os.environ["SQL_PASSWORD"]
def get_driver():
    return os.environ["ODBC_DRIVER"]
def get_predicted_games_query(sports_book: str):
    predicted_games_query = "SELECT TOP(8) [dbo].[PredictedGame].[id],[gameDate],[" + sports_book \
                            + "VegasHomeOdds],[" + sports_book + "VegasAwayOdds]," \
                            "[home].[abbreviation]," \
                            "[away].[abbreviation]" \
                            "FROM [dbo].[PredictedGame] " \
                            "INNER JOIN dbo.Team home ON home.id = homeTeamId " \
                            "INNER JOIN dbo.Team away ON away.id = awayTeamId " \
                            "WHERE " + sports_book + "VegasAwayOdds=0 AND " + sports_book + "VegasHomeOdds=0"
    return predicted_games_query
def get_connection_string():
    return 'DRIVER='+get_driver()+';SERVER=tcp:'+get_server()+';PORT=1433;DATABASE='+get_database()+';UID='+get_username()+';PWD='+get_password()

def get_predicted_games(sports_book: str) -> list[PredictedGame]:
    games = []
    # Grab all entries from sql
    with pyodbc.connect(get_connection_string()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(get_predicted_games_query(sports_book))
            row = cursor.fetchone()
            while row:
                games.append(row)
                row = cursor.fetchone()
    return predicted_game_mapper.map_db_predicted_games_to_entities(games)

def store_probability(game: PredictedGame, sports_book):
    with pyodbc.connect(get_connection_string()) as conn:
        with conn.cursor() as cursor:
            query = "UPDATE PredictedGame SET " + sports_book + "VegasHomeOdds = " + str(game.get_home_odds()) \
                    + ", " + sports_book + "VegasAwayOdds = " + str(game.get_away_odds()) + "WHERE id = " + str(game.id)
            cursor.execute(query)
