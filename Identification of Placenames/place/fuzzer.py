from fuzzywuzzy import fuzz
import csv


def data_extract(filename):
    places = {}
    with open(filename, 'r', encoding='utf-8', errors='ignore') as fh:
        reader = csv.reader(fh)
        header = next(reader)  # Skip the header row

        for row in reader:
            country = row[0].strip() if row[0] else ''
            state = row[1].strip() if row[1] else ''
            city = row[2].strip() if row[2] else ''

            # Extract the main part of the place name
            place_name = f"{country}, {state}, {city}".strip(', ').split(',')[0].strip()

            places[place_name] = {
                'country': country,
                'state': state,
                'city': city
            }

    return places


def find_closest_match(input_word, location_dict):
    max_similarity = 0
    closest_match = None
    level = None

    for location, levels in location_dict.items():
        country_similarity = fuzz.ratio(input_word, levels['country'])
        state_similarity = fuzz.ratio(input_word, levels['state'])
        city_similarity = fuzz.ratio(input_word, levels['city'])

        if country_similarity > max_similarity:
            max_similarity = country_similarity
            closest_match = location
            level = 'Country'
        if state_similarity > max_similarity:
            max_similarity = state_similarity
            closest_match = location
            level = 'State'
        if city_similarity > max_similarity:
            max_similarity = city_similarity
            closest_match = location
            level = 'City'

    return closest_match, level


def fuzzy_search(file, word):
    places = data_extract(file)
    fuzzy, level = find_closest_match(word, places)
    canonical_name = fuzzy  # The canonical name is the fuzzy match itself
    return [word, canonical_name, level]
