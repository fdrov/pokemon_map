import folium
from folium.plugins import MarkerCluster
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from pokemon_entities.models import PokemonEntity, Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, title, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally to fix strange folium cyrillic encoding bug
        icon=icon, popup=title
    ).add_to(folium_map)



def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(folium_map)
    for pokemon in pokemons:
        pokemon_entities = pokemon.pokemon_entities.all()
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                marker_cluster,
                pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon_entity.pokemon.title,
                request.build_absolute_uri(pokemon_entity.pokemon.picture.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.picture:
            pic_url = pokemon.picture.url
        else:
            pic_url = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pic_url),
            'title_ru': pokemon.title,
        })
    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = pokemon.pokemon_entities.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.title,
            request.build_absolute_uri(pokemon_entity.pokemon.picture.url)
        )
    element_type = []
    elements = pokemon.element_type.all()
    for element in elements:
        element_type.append({
            'title': element.title,
            'img': element.image.url,
            'strong_against': [el for el in element.strong_against.all()]
        }
        )
    pokemon_info = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.picture.url,
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'element_type': element_type
    }
    if pokemon.previous_evolution:
        pokemon_info['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': pokemon.previous_evolution.picture.url
        }
    if pokemon.next_evolution.all():
        pokemon = pokemon.next_evolution.first()
        pokemon_info['next_evolution'] = {
            'title_ru': pokemon.title,
            'pokemon_id': pokemon.id,
            'img_url': pokemon.picture.url
        }

    return render(request, "pokemon.html",
                  context={'map': folium_map._repr_html_(),
                           'pokemon': pokemon_info})
