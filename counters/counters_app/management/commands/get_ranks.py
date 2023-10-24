from django.core.management.base import BaseCommand
from counters_app.models import Hero
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Scrape hero win rates and update their ranks in the current patch'

    def handle(self, *args, **kwargs):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        url = 'https://www.dotabuff.com/heroes/meta'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'class': 'sortable no-arrows r-tab-enabled'})

        rows = table.find_all('tr')

        heroes = []

        for row in rows:
            cells = row.find_all('td')

            if len(cells) < 12:
                continue

            hero_name = cells[1].get_text()

            last_winrate = cells[-1]['data-value']

            heroes.append({'name': hero_name, 'winrate': last_winrate})

            heroes_sorted = sorted(heroes, key=lambda x: x['winrate'], reverse=True)

        for i, hero in enumerate(heroes_sorted):
            hero['rating'] = i + 1

        for hero in heroes_sorted:
            hero_name_db_format = hero['name'].lower().replace(' ', '-').replace("'", "")

            try:
                hero_obj = Hero.objects.get(name=hero_name_db_format)
                hero_obj.rank = hero['rating']
                hero_obj.save()

            except Hero.DoesNotExist:
                print(f"Hero {hero['name']} not found in the database.")

