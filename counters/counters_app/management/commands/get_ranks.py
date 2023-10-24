from django.core.management.base import BaseCommand
from counters_app.models import Hero
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Scrape hero win rates and update their ranks in the current patch'

    def handle(self, *args, **kwargs):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # Здесь ваш код для скрапинга данных (я использую requests и BeautifulSoup для примера)
        url = 'https://www.dotabuff.com/heroes/meta'  # Замените на URL источника данных
        response = requests.get(url, headers=headers)
        # Предположим, что 'html_content' содержит HTML-код страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим таблицу
        table = soup.find('table', {'class': 'sortable no-arrows r-tab-enabled'})

        # Находим все строки в таблице
        rows = table.find_all('tr')

        heroes = []

        # Проходим по каждой строке
        for row in rows:
            # Находим все ячейки в строке
            cells = row.find_all('td')

            # Если в строке меньше 12 ячеек, пропускаем её
            if len(cells) < 12:
                continue

            # Извлекаем имя героя
            hero_name = cells[1].get_text()

            # Извлекаем последний винрейт (он находится в 12-й ячейке)
            last_winrate = cells[-1]['data-value']

            heroes.append({'name': hero_name, 'winrate': last_winrate})

            # Сортируем список героев по винрейту в порядке убывания
            heroes_sorted = sorted(heroes, key=lambda x: x['winrate'], reverse=True)

            # Присваиваем рейтинг каждому герою
        for i, hero in enumerate(heroes_sorted):
            hero['rating'] = i + 1

        # Выводим отсортированный список героев с рейтингами
        for hero in heroes_sorted:
            hero_name_db_format = hero['name'].lower().replace(' ', '-').replace("'", "")

            try:
                hero_obj = Hero.objects.get(name=hero_name_db_format)
                hero_obj.rank = hero['rating']
                hero_obj.save()

            except Hero.DoesNotExist:
                print(f"Hero {hero['name']} not found in the database.")

