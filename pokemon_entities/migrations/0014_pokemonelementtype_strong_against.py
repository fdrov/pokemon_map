# Generated by Django 3.1.8 on 2021-04-20 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0013_pokemonelementtype_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='strong_against',
            field=models.ManyToManyField(default=None, null=True, to='pokemon_entities.PokemonElementType'),
        ),
    ]
