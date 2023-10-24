import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from counters_app.models import Hero, HeroCounters


class Command(BaseCommand):
    help = 'Collect counter picks for all heroes'

    def handle(self, *args, **kwargs):
        hero_list = ['anti-mage', 'axe', 'bane', 'bloodseeker', 'crystal-maiden', 'drow-ranger', 'earthshaker',
                     'juggernaut', 'mirana', 'morphling', 'shadow-fiend', 'phantom-lancer', 'puck', 'pudge', 'razor',
                     'sand-king', 'storm-spirit', 'sven', 'tiny', 'vengeful-spirit', 'windranger', 'zeus', 'kunkka',
                     'lina', 'lion', 'shadow-shaman', 'slardar', 'tidehunter', 'witch-doctor', 'lich', 'riki', 'enigma',
                     'tinker', 'sniper', 'necrophos', 'warlock', 'beastmaster', 'queen-of-pain', 'venomancer',
                     'faceless-void', 'wraith-king', 'death-prophet', 'phantom-assassin', 'pugna', 'templar-assassin',
                     'viper', 'luna', 'dragon-knight', 'dazzle', 'clockwerk', 'leshrac', "natures-prophet",
                     'lifestealer', 'dark-seer', 'clinkz', 'omniknight', 'enchantress', 'huskar', 'night-stalker',
                     'broodmother', 'bounty-hunter', 'weaver', 'jakiro', 'batrider', 'chen', 'spectre',
                     'ancient-apparition', 'doom', 'ursa', 'spirit-breaker', 'gyrocopter', 'alchemist', 'invoker',
                     'silencer', 'outworld-destroyer', 'lycan', 'brewmaster', 'shadow-demon', 'lone-druid',
                     'chaos-knight', 'meepo', 'treant-protector', 'ogre-magi', 'undying', 'rubick', 'disruptor',
                     'nyx-assassin', 'naga-siren', 'keeper-of-the-light', 'io', 'visage', 'slark', 'medusa',
                     'troll-warlord', 'centaur-warrunner', 'magnus', 'timbersaw', 'bristleback', 'tusk',
                     'skywrath-mage', 'abaddon', 'elder-titan', 'legion-commander', 'techies', 'ember-spirit',
                     'earth-spirit', 'underlord', 'terrorblade', 'phoenix', 'oracle', 'winter-wyvern', 'arc-warden',
                     'monkey-king', 'dark-willow', 'pangolier', 'grimstroke', 'hoodwink', 'void-spirit', 'snapfire',
                     'mars', 'dawnbreaker', 'marci', 'primal-beast', 'muerta']

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'}

        for hero_name in hero_list:
            # 1. Запрос страницы
            url = f'https://www.dotabuff.com/heroes/{hero_name}/counters'
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                table = soup.find('table', {'class': 'sortable'})

                standardized_hero_name = hero_name.lower().replace(" ", "-").replace("'", "")

                hero, created = Hero.objects.get_or_create(name=hero_name)

                for i, row in enumerate(table.find_all('tr')[1:]):
                    cells = row.find_all('td')
                    counter_hero_name = cells[1].text.strip().lower().replace(" ", "-").replace("'", "")

                    counter_hero, created = Hero.objects.get_or_create(name=counter_hero_name)

                    HeroCounters.objects.update_or_create(
                        hero=hero,
                        counter_hero=counter_hero,
                        defaults={
                            'rank': i + 1  # Мы предполагаем, что таблица уже отсортирована
                        }
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully updated counter for {hero_name} against {counter_hero_name}'))

            else:
                self.stdout.write(self.style.ERROR(f'Failed to get data from {url}, status code: {response.status_code}'))

