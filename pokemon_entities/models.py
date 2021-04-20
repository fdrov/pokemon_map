from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField(max_length=200, verbose_name='Стихия')
    image = models.ImageField(verbose_name='Эмблема стихии',
                              null=True, default=None, blank=True)
    strong_against = models.ManyToManyField('self',
                                            symmetrical=False,
                                            default=None,
                                            null=True,
                                            blank=True)

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    picture = models.ImageField(verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    title_en = models.CharField(max_length=200, blank=True,
                                verbose_name='имя на английском')
    title_jp = models.CharField(max_length=200, blank=True,
                                verbose_name='имя на японском')
    previous_evolution = models.ForeignKey('self', blank=True, null=True,
                                           on_delete=models.SET_NULL,
                                           related_name='next_evolution',
                                           verbose_name='Предыдущая форма')
    element_type = models.ManyToManyField(PokemonElementType)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                verbose_name='Покемон',
                                related_name='pokemon_entities')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился', blank=True,
                                       null=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчез', blank=True,
                                          null=True)
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True,
                                  null=True)

    def __str__(self):
        return f'{self.pokemon.title}, уровень {self.level}, ID = {self.id}'
