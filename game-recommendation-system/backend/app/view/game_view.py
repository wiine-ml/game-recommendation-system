from flask_admin.contrib.sqla import ModelView

class GameView(ModelView):
    column_list = ('id', 
                   'gameTitle', 
                   'gameGenre', 
                   'gamePlatform', 
                   'releaseYear', 
                   'releaseMonth', 
                   'releaseDay'
                   'ratingPhrase', 
                   'followers', 
                   'rating', 
                   'officalRating', 
                   'gameUrl', 
                   'gameDeveloper', 
                   'gamePublisher', 
                   'gameImage'
                   )