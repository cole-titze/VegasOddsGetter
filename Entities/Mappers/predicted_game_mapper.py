from Entities import predicted_game

def map_db_predicted_games_to_entities(games: list) -> list:
    clean_games = []
    for game in games:
        clean_game = predicted_game.PredictedGame(
            id=game[0],
            gameDate=game[1],
            vegasHomeOdds=game[2],
            vegasAwayOdds=game[3],
            homeTeamAbbreviation=game[4],
            awayTeamAbbreviation=game[5]
        )
        clean_games.append(clean_game)
    return clean_games
