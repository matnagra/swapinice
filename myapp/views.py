from django.shortcuts import render
import requests

class Pelicula:
  def __init__(self, peli):
    self.id = peli["episode_id"]
    self.title = peli["title"]
    self.ano = peli["release_date"][0:4]
    self.director = peli["director"]
    self.producer = peli["producer"]
    self.url = peli['url']

  def load_pelicula(self, peli):
    self.opening = peli["opening_crawl"]

class Actor:
  def __init__(self, actor):
    self.name = actor['name']
    self.url = actor['url']

  def load_actor(self, actor):
    self.height = actor['height']
    self.mass = actor['mass']
    self.hair = actor['hair_color']
    self.skin = actor['skin_color']
    self.eye = actor['eye_color']
    self.birth = actor['birth_year']
    self.gender = actor['gender']
    self.homeworld = self.load_homeworld(actor)

  def load_homeworld(self, actor):
    response = requests.get(actor['homeworld'])
    homeworld_json = response.json()
    return homeworld_json['name']

class Ship:
  def __init__(self, ship):
    self.name = ship['name']
    self.url = ship['url']
  def load_ship(self, ship):
    self.model = ship['model']
    self.manufacturer = ship['manufacturer']
    self.cost_in_credits = ship['cost_in_credits']
    self.length = ship['length']
    self.max_atmosphering_speed = ship['max_atmosphering_speed']
    self.crew = ship['crew']
    self.passengers = ship['passengers']
    self.cargo_capacity = ship['cargo_capacity']
    self.consumables = ship['consumables']
    self.hyperdrive_rating = ship['hyperdrive_rating']
    self.mglt = ship['MGLT']
    self.starship_class = ship['starship_class']


class Planet:
  def __init__(self, planet):
    self.name = planet['name']
    self.url = planet['url']

  def load_planet(self, planet):
    self.rotation_period = planet['rotation_period']
    self.orbital_period = planet['orbital_period']
    self.diameter = planet['diameter']
    self.climate = planet['climate']
    self.gravity = planet['gravity']
    self.terrain = planet['terrain']
    self.surface_water = planet['surface_water']
    self.population = planet['population']

class Search:
    def __init__(self, name, url):
        self.name = name
        self.url = url


# Create your views here.
def index(request):

    response = requests.get('https://swapi.co/api/films')
    films = response.json()
    peliculas = list()
    for peli in films["results"]:
        p = Pelicula(peli)
        peliculas.append(p)

    return render(request, 'index.html', {'data': peliculas})


def film(request):

    film_url = request.GET.get('url', '')

    response = requests.get(film_url)
    peli = response.json()
    pelicula = Pelicula(peli)
    pelicula.load_pelicula(peli)

    url_actores = peli['characters']
    actores = list()
    for url in url_actores:
        response = requests.get(url)
        persona = response.json()
        actor = Actor(persona)
        actores.append(actor)

    url_ships = peli['starships']
    ships = list()
    for url in url_ships:
        response = requests.get(url)
        ship_json = response.json()
        ship = Ship(ship_json)
        ships.append(ship)

    url_planets = peli['planets']
    planets = list()
    for url in url_planets:
        response = requests.get(url)
        planet_json = response.json()
        planet = Ship(planet_json)
        planets.append(planet)

    return render(request, 'film.html', {'pelicula':pelicula, 'actores':actores, 'ships':ships, 'planets':planets})

def actor(request):

    actor_url = request.GET.get('url', '')

    response = requests.get(actor_url)
    actor_json = response.json()
    actor = Actor(actor_json)
    actor.load_actor(actor_json)

    url_films = actor_json['films']
    films = list()
    for url in url_films:
        response = requests.get(url)
        film = response.json()
        peli = Pelicula(film)
        films.append(peli)

    url_ships = actor_json['starships']
    ships = list()
    for url in url_ships:
        response = requests.get(url)
        ship_json = response.json()
        ship = Ship(ship_json)
        ships.append(ship)

    return render(request, 'actor.html', {'actor':actor, 'films':films, 'ships':ships})

def ship(request):

    ship_url = request.GET.get('url', '')
    response = requests.get(ship_url)
    ship_json = response.json()
    ship = Ship(ship_json)
    ship.load_ship(ship_json)

    url_pilots = ship_json['pilots']
    pilots = list()
    for url in url_pilots:
        response = requests.get(url)
        pilot_json = response.json()
        pilot = Actor(pilot_json)
        pilots.append(pilot)

    url_films = ship_json['films']
    films = list()
    for url in url_films:
        response = requests.get(url)
        film_json = response.json()
        film = Pelicula(film_json)
        films.append(film)

    return render(request, 'ship.html', {'ship':ship, 'pilots':pilots, 'films':films})

def planet(request):
    planet_url = request.GET.get('url', '')

    response = requests.get(planet_url)
    planet_json = response.json()
    planet = Planet(planet_json)
    planet.load_planet(planet_json)

    url_residents = planet_json['residents']
    residents = list()
    for url in url_residents:
        response = requests.get(url)
        resident_json = response.json()
        resident = Actor(resident_json)
        residents.append(resident)

    url_films = planet_json['films']
    films = list()
    for url in url_films:
        response = requests.get(url)
        films_json = response.json()
        film = Pelicula(films_json)
        films.append(film)

    return render(request, 'planet.html', {'planet': planet, 'residents':residents, 'films':films})

def search(request):
    selection = request.GET.get('selection', '')
    text = request.GET.get('text', '')

    people_result = list()
    starships_result = list()
    films_result = list()
    planets_result = list()

    def look_up(url):
        response = requests.get(url)
        json = response.json()
        resultado_local = json['results']

        search_result = list()
        for elem in resultado_local:
            if "films" in url:
                search_result.append(Search(elem['title'], elem['url']))
            else:
                search_result.append(Search(elem['name'], elem['url']))

        if json['next'] != None:
            search_result.extend(look_up(json['next']))

        return search_result

    if selection == "people":
        new_url = "https://swapi.co/api/people/?search="+text
        people_result = look_up(new_url)

    elif selection == "starships":
        new_url = "https://swapi.co/api/starships/?search="+text
        starships_result = look_up(new_url)

    elif selection == "films":
        new_url = "https://swapi.co/api/films/?search="+text
        films_result = look_up(new_url)

    elif selection == "planets":
        new_url = "https://swapi.co/api/planets/?search="+text
        planets_result = look_up(new_url)

    else:
        new_url = "https://swapi.co/api/people/?search=" + text
        people_result = look_up(new_url)

        new_url = "https://swapi.co/api/starships/?search=" + text
        starships_result = look_up(new_url)

        new_url = "https://swapi.co/api/films/?search=" + text
        films_result = look_up(new_url)

        new_url = "https://swapi.co/api/planets/?search=" + text
        planets_result = look_up(new_url)

    return render(request, 'search.html', {'selection':selection, 'people_result':people_result,
                                           'starships_result':starships_result, 'films_result':films_result,
                                           'planets_result':planets_result})
