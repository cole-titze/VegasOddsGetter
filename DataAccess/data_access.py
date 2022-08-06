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
def get_predicted_games_query():
    predicted_games_query = "SELECT [dbo].[PredictedGame].[id],[gameDate],[vegasHomeOdds],[vegasAwayOdds]," \
                            "[home].[abbreviation]," \
                            "[away].[abbreviation]" \
                            "FROM [dbo].[PredictedGame] " \
                            "INNER JOIN dbo.Team home ON home.id = homeTeamId " \
                            "INNER JOIN dbo.Team away ON away.id = awayTeamId " \
                            "WHERE vegasAwayOdds=0 AND vegasHomeOdds=0"
    return predicted_games_query
def get_connection_string():
    return 'DRIVER='+get_driver()+';SERVER=tcp:'+get_server()+';PORT=1433;DATABASE='+get_database()+';UID='+get_username()+';PWD='+get_password()

def get_predicted_games() -> list[PredictedGame]:
    games = []
    # Grab all entries from sql
    with pyodbc.connect(get_connection_string()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(get_predicted_games_query())
            row = cursor.fetchone()
            while row:
                games.append(row)
                row = cursor.fetchone()
    return predicted_game_mapper.map_db_predicted_games_to_entities(games)

def store_probabilities(games: list[PredictedGame]):
    for game in games:
        with pyodbc.connect(get_connection_string()) as conn:
            with conn.cursor() as cursor:
                query = "UPDATE PredictedGame SET vegasHomeOdds = " + str(game.get_home_odds()) + ", vegasAwayOdds = " + str(game.get_away_odds()) + "WHERE id = " + str(game.id)
                cursor.execute(query)