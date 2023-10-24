from django.db import models


class Hero(models.Model):
    name = models.CharField(max_length=50)
    rank = models.IntegerField(null=True, blank=True)
    roles = models.JSONField(null=True, blank=True)


class HeroCounters(models.Model):
    hero = models.ForeignKey(Hero, related_name='hero_counters', on_delete=models.CASCADE)
    counter_hero = models.ForeignKey(Hero, related_name='countered_by', on_delete=models.CASCADE)
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('hero', 'counter_hero')
