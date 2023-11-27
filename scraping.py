# importing libraries

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd


# function for data scraping

def scraping(driver):

    html_content = driver.page_source

    driver.implicitly_wait(10)

    # using BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')

    section_matches = soup.find('section', class_="tabela__listao")
    title_round = section_matches.find('span', class_="lista-jogos__navegacao--rodada").text

    round_ = title_round.split()[0]

    if len(round_) == 3:
        round_ = int(round_[0:2])
    else:
        round_ = int(round_[0:1])

    matchdays = soup.find('ul', class_='lista-jogos')

    matchs = matchdays.find_all('li')

    away_teams = []
    home_teams = []
    places = []
    away_scores = []
    home_scores = []

    for match_div in matchs:
        home = match_div.find('div', class_='placar__equipes--mandante')
        home_team = home.find('span', class_='equipes__nome').text

        away = match_div.find('div', class_='placar__equipes--visitante')
        away_team = away.find('span', class_='equipes__nome').text

        place = match_div.find('span', class_='jogo__informacoes--local').text

        home_teams.append(home_team)
        away_teams.append(away_team)

        places.append(place)

        score_match = match_div.find('div', class_='placar-box')
        home_score = score_match.find('span', class_='placar-box__valor--mandante').text
        away_score = score_match.find('span', class_='placar-box__valor--visitante').text

        home_score = int(home_score) if home_score != '' else None
        away_score = int(away_score) if away_score != '' else None

        home_scores.append(home_score)
        away_scores.append(away_score)

    round_list = [round_ for i in range(len(home_teams))]

    data = {
        'round': round_list,
        'stadium': places,
        'home_team': home_teams,
        'home_score': home_scores,
        'away_score': away_scores,
        'away_team': away_teams
    }

    print(len(round_list))
    print(len(places))
    print(len(home_teams))
    print(len(home_scores))
    print(len(away_scores))
    print(len(away_teams))

    datas = pd.DataFrame(data)

    print(datas)

    return datas


# making a list to go through the years and automate the scraping


years = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
         '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']

for year in years:

    # creating a Chrome driver

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    url = f"https://ge.globo.com/futebol/brasileirao-serie-a/20{year}/"

    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(15)

    btn_left = driver.find_element("xpath", '//*[@id="classificacao__wrapper"]/section/nav/span[1]')

    if year in ['03', '04']:
        range_ = 46
    elif year == '05':
        range_ = 42
    else:
        range_ = 38

    for i in range(range_):
        time.sleep(5)
        driver.implicitly_wait(1)
        btn_left.click()

    time.sleep(0.5)

    df = scraping(driver)

    btn_right = driver.find_element("xpath", '//*[@id="classificacao__wrapper"]/section/nav/span[3]')

    for i in range(range_):
        time.sleep(5)
        btn_right.click()
        df_concat = scraping(driver)

        df = pd.concat([df, df_concat], ignore_index=True)

        df.to_csv(f'datas/brasileirao_20{year}.csv', index=False)

    time.sleep(1)

    print('-' * 50)
    print('Ano: 20' + year)
    print(df.shape)
    print(df.head())
    print('-' * 50)

    driver.quit()