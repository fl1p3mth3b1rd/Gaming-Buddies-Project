from gaming_buddies import create_app
from gaming_buddies.get_game_list_from_steam import get_games

app = create_app()
with app.app_context():
    get_games()