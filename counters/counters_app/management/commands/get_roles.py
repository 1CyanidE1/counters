import requests
from bs4 import BeautifulSoup
import re


from django.core.management.base import BaseCommand
from counters_app.models import Hero


class Command(BaseCommand):
    help = 'Collect roles for all heroes'

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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'
        }
        for hero_name in hero_list:
            lanes = {}
            for page_number in range(1, 5):
                url = f'https://www.dotabuff.com/heroes/{hero_name}/guides?page={page_number}'
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    groups = soup.find_all('div', {'class': 'kv kv-label'})

                    for group in groups:
                        lane_icon = group.find('i', {'class': re.compile('fa-lane-')})
                        role_icon = group.find('i', {'class': re.compile('fa-role-')})

                        if lane_icon:
                            lane = lane_icon.get('title')
                            if lane not in lanes:
                                lanes[lane] = []

                        if role_icon:
                            role = role_icon.get('title')
                            if role not in lanes[lane]:
                                lanes[lane].append(role)

                    try:
                        hero_obj = Hero.objects.get(name=hero_name)
                        hero_obj.roles = lanes
                        hero_obj.save()

                    except Hero.DoesNotExist:
                        print(f"Hero {hero_name} not found in the database.")

                else:
                    print(f"Failed to get data from {url}, status code: {response.status_code}")

        print('Result', lanes)
