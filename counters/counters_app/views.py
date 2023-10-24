from django.shortcuts import render
from django.db.models import F

from .models import Hero, HeroCounters


def counter_picks(request):
    all_heroes = Hero.objects.all().order_by('name')
    use_meta = request.GET.get('use_meta') == 'on'
    weight_meta = 0.7
    weight_rank = 0.3

    if 'hero_id' in request.GET:
        hero_id = request.GET.get('hero_id')
        selected_hero = Hero.objects.get(id=hero_id)

        if use_meta:
            counter_picks = HeroCounters.objects.filter(hero=selected_hero).annotate(
                combined_rank=F('rank') * weight_meta + F('counter_hero__rank') * weight_rank
            ).order_by('combined_rank')
        else:
            counter_picks = HeroCounters.objects.filter(hero=selected_hero).order_by('rank')

        counter_picks = list(counter_picks)

        for i, counter in enumerate(counter_picks):
            counter.position = i + 1

        return render(request, 'counter_picks.html', {
            'counter_picks': counter_picks,
            'selected_hero': selected_hero,
            'all_heroes': all_heroes,
            'use_meta': use_meta
        })
    else:
        return render(request, 'counter_picks.html', {'all_heroes': all_heroes})


def index(request):
    return render(request, 'index.html')


def meta(request):
    all_heroes = Hero.objects.all().order_by('name')
    return render(request, 'meta.html', {'all_heroes': all_heroes})
