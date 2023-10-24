from django.shortcuts import render
from .models import Hero, HeroCounters


def counter_picks(request):
    all_heroes = Hero.objects.all().order_by('name')
    weight_meta = 0.7
    weight_rank = 0.3

    if 'hero_id' in request.GET:
        hero_id = request.GET.get('hero_id')
        selected_hero = Hero.objects.get(id=hero_id)

        # Получение контр-пики
        counter_picks = HeroCounters.objects.filter(hero=selected_hero)

        # Добавление рангов и сортировка
        counter_picks_with_ranks = []
        for counter in counter_picks:
            counter_hero = counter.counter_hero
            combined_rank = counter.rank * weight_meta + counter_hero.rank * weight_rank
            counter_picks_with_ranks.append({
                'counter_hero': counter_hero,
                'counter_rank': counter.rank,
                'hero_rank_in_patch': counter_hero.rank,
                'combined_rank': combined_rank
            })

        # Сортировка по комбинированному рангу
        sorted_counter_picks = sorted(counter_picks_with_ranks, key=lambda x: x['combined_rank'])

        return render(request, 'counter_picks.html', {'counter_picks': sorted_counter_picks, 'selected_hero': selected_hero, 'all_heroes': all_heroes})
    else:
        return render(request, 'counter_picks.html', {'all_heroes': all_heroes})
