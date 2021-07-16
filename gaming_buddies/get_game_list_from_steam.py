from gaming_buddies.model import GameInformation, db
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common.exceptions import ErrorInResponseException
from urllib.request import urlretrieve
import os

def get_html(url):
    try:
        chromedriver = 'C:\chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(executable_path=chromedriver, options=options)
        browser.get(url)
        return browser.page_source
    except(ErrorInResponseException, ValueError):
        print("Сеетевая ошибка")
        return False

def get_games():
    html = get_html('https://store.steampowered.com/?l=russian')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        game_types_parsed = soup.find('div', {'class':'popup_genre_expand_content responsive_hidden', 'data-genre-group':'social_and_players'}).findAll('a')
        game_types_urls = []
        game_types = []
        pages_to_parse = 10
        games_for_each_type = {}
        pattern = r'\?(.*)'
        for game_type in game_types_parsed:
            if "Одиночная игра" not in game_type.text:
                url = re.sub(pattern,"", game_type.get('href'))
                games_for_each_type[game_type.text] = {}
                for page in range(pages_to_parse):
                    game_types.append(game_type.text)
                    game_types_urls.append(url.strip() + f'#p={page}&tab=ConcurrentUsers')
    get_games_for_each_game_type(game_types_urls, game_types, games_for_each_type)

def get_games_for_each_game_type(game_types_urls, game_types, games_for_each_type):
    for i, url in enumerate(game_types_urls):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            games = soup.find('div', id='ConcurrentUsersRows').findAll('a')
            for game in games:
                game_name = game.find('div', class_='tab_item_name').text
                game_logo_url = game.find('img', class_='tab_item_cap_img')['src']
                games_for_each_type[game_types[i]][game_name] = game_logo_url
    for game_type in games_for_each_type:
        for game, logo_url in games_for_each_type[game_type].items():
            save_games(game_type, game, logo_url)

def save_games(genre, game, logo_url):
    existing_games = GameInformation.query.filter(GameInformation.name==game).count()
    if not existing_games:
        game_name = re.sub(r'[^a-zA-Z0-9 ]+', '', game).strip()
        actual_directory = os.path.abspath(os.path.abspath(__file__))
        actual_directory = os.path.join(actual_directory, '..', 'static', 'game_logos', game_name + '.jpg')
        urlretrieve(logo_url, actual_directory)
        directory = "/static/game_logos/" + game_name + '.jpg'
        new_games = GameInformation(genre=genre, name=game, game_logo_dir=directory, proper_name=game_name.lower())
        db.session.add(new_games)
        db.session.commit()
