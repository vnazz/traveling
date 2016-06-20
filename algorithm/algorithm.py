import random
from collections import defaultdict
import copy
import math

cities = {"New York City": {"lat": 40.7128, "lng": -74.0059},
          "Los Angeles": {"lat": 34.0522, "lng": -118.2437},
          "Chicago": {"lat": 41.8781, "lng": -87.6298},
          "Houston": {"lat": 29.7604, "lng": -95.3698},
          "Philadelphia": {"lat": 39.9526, "lng": -75.1652},
          "Phoenix": {"lat": 33.4484, "lng": -112.0740},
          "San Antonio": {"lat": 29.4241, "lng": -98.4936},
          "San Diego": {"lat": 32.7157, "lng": -117.1611},
          "Dallas": {"lat": 32.7767, "lng": -96.7970},
          "San Jose": {"lat": 37.3382, "lng": -121.8863},
          "Austin": {"lat": 30.2672, "lng": -97.7431},
          "Jacksonville": {"lat": 30.3322, "lng": -81.6557},
          "Indianapolis": {"lat": 39.7684, "lng": -86.1581},
          "San Francisco": {"lat": 37.7749, "lng": -122.4194}
    ,     "Columbus": {"lat": 39.9612, "lng": -82.9988},
          "Fort Worth": {"lat": 32.7555, "lng": -97.3308},
          "Charlotte": {"lat": 35.2271, "lng": -80.8431},
          "Detroit": {"lat": 42.3314, "lng": -83.0458},
          "El Paso": {"lat": 31.7619, "lng": -106.4850},
          "Memphis": {"lat": 35.1495, "lng": -90.0490},
          "Boston": {"lat": 42.3601, "lng": -71.0589},
          "Seattle": {"lat": 47.6062, "lng": -122.3321},
          "Denver": {"lat": 39.7392, "lng": -104.9903},
          "Washington D.C": {"lat": 38.9072, "lng": -77.0369},
          "Nashville": {"lat": 36.1627, "lng": -86.7816},
          "Baltimore": {"lat": 39.2904, "lng": -76.6122},
          "Louisville": {"lat": 38.2527, "lng": -85.7585},
          "Portland": {"lat": 45.5231, "lng": -122.6765},
          "Oklahoma City": {"lat": 35.0078, "lng": -97.0929},
          "Milwaukee": {"lat": 43.0389, "lng": -87.9065}}

paths = []

def calculateDistanceBetweenTwo(city1, city2):
    """
    This function is based on http://andrew.hedges.name/experiments/haversine/
    It uses the latitude and longitude of two locations to find the distance between them.
    :param city1: The first dictionary entry with longitude and latitude
    :param city2: The second dictionary entry with longitude and latitude
    :return: The distance between city1 and city2
    """
    longs = math.radians(cities[city2]["lng"] - cities[city1]["lng"])
    lats = math.radians(cities[city2]["lat"] - cities[city1]["lat"])
    lat1 = math.radians(cities[city1]["lat"])
    lat2 = math.radians(cities[city2]["lat"])

    a = math.sin(lats / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(longs / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 3961 * c

    return distance


def initialize():
    """
    Creates 500 random paths that include the 30 most populous cities in the US.
    :return: None
    """
    i = 0;
    while i < 500:
        path = []
        while len(path) < len(cities.keys()):
            choice = random.choice(cities.keys())
            if choice not in path:
                path.append(choice)
        paths.append(path)
        i += 1;


def scorePortion(path, start, end):
    """
    Scores a portion of a path.
    :param path: The path that will have a portion scored
    :param start: The index of the first entry that will be scored
    :param end: The index of the last entry that will be scored
    :return: The score of the portion of path starting at start and including end
    """
    score = 0
    for i in range(start, end):
        score += calculateDistanceBetweenTwo(path[i], path[i + 1])
    return score


def score(path):
    """
    Scores the entire path.
    :param path: the path that will be scored
    :return: the distance of the path that was given
    """
    score = 0;
    for i in range(len(path) - 1):
        score += calculateDistanceBetweenTwo(path[i], path[i + 1])
    return score


def scoreAll(paths):
    """
    Scores all the paths given.
    :param paths: The paths that will be scored
    :return: A dictionary with distances as keys and paths as values
    """
    scores = defaultdict(list)
    for path in paths:
        scores[score(path)].append(path)
    return scores

def createNextGen():
    """
    Creates a new generation by randomly choosing two paths and crossing them.
    :return: A new list of paths based on the current generation of paths
    """
    availParents = []
    j = 0
    while j < 2:
        for i in range(len(paths)):
            availParents.append(i)
        j += 1
    nextGen = []
    while len(nextGen) < len(paths):
        parent1 = random.choice(availParents)
        availParents.remove(parent1)
        parent2 = random.choice(availParents)
        availParents.remove(parent2)

        nextGen.append(createChild(paths[parent1], paths[parent2]))
    return nextGen


def createChild(parent1, parent2):
    """
    Creates a child given two parents by picking a range of indices and
    picking the parent with the lowest distance in the range. Then the other
    parent's cities that were not in the range are taken in order to create
    the child.
    :param parent1: A path of cities
    :param parent2: Another path of cities
    :return: A child based on the algorithm described above
    """
    start = random.randint(0, len(parent1) / 4)
    score1 = scorePortion(parent1, start, len(parent1) / 2 + 1)
    score2 = scorePortion(parent2, start, len(parent2) / 2 + 1)
    if (score1 < score2):
        optimalSection = parent1[start: len(parent1) / 2 + 2]
        remainingCities = getRemainingCities(optimalSection, parent2)
        child = insertCities(start, optimalSection, remainingCities)
    else:
        optimalSection = parent2[start: len(parent2) / 2 + 2]
        remainingCities = getRemainingCities(optimalSection, parent1)
        child = insertCities(start, optimalSection, remainingCities)

    child = mutation(child)
    return child


def getRemainingCities(section, otherParent):
    """
    Generates a list of cities that are not in section.
    :param section: A list of cities
    :param otherParent: A list of cities
    :return: A list of the cities not in section but are in otherParent
    """
    remaining = []
    for i in range(len(otherParent)):
        if otherParent[i] not in section:
            remaining.append(otherParent[i])

    return remaining


def insertCities(start, section, remainingCities):
    """
    Inserts "remainingCities" around the section that was given.
    :param start: The starting point of section
    :param section: A list of cities
    :param remainingCities: A list of cities that are not in section
    :return: A child that has all 30 cities and contains section and remainingCities
    """
    child = []
    i = 0
    while i < start:
        child.append(remainingCities[i])
        i += 1
    child.extend(section)
    while i < len(remainingCities):
        child.append(remainingCities[i])
        i += 1
    return child

def mutation(child):
    """
    There is a 10% chance of mutation. A mutation swaps the order of two cities.
    :param child: A list of cities that may be mutated
    :return: A list of cities that might have been changed
    """
    mutation = random.random()
    if mutation < 0.10:
        position = random.randint(0, len(child) - 2)
        temp = child[position]
        child[position] = child[position + 1]
        child[position + 1] = temp
    return child


def runsimulation(times):
    """
    Makes "times" generations of paths.
    :param times: The number of generations that will be made
    :return: None
    """
    global paths
    for i in range(times):
        nextGen = createNextGen()
        paths = copy.deepcopy(nextGen)


def findOptima(scores):
    """
    Finds the path(s) with the lowest score.
    :param scores: A dictionary that contains all the paths and their scores
    :return: A tuples of the lowest score and the path associated with it
    """
    topScore = min(scores)
    topPath = scores[topScore]
    return (topScore, topPath)

def main():
    """
    Makes 10,000 generations and prints out the path(s) with the lowest distance of the final generation.
    :return: None
    """
    initialize()
    runsimulation(10000)
    scores = scoreAll(paths)
    optimalScore, optimalPath = findOptima(scores)
    if len(optimalPath) is 1:
        print ("The optimal path is {} with a score of {}".format(optimalPath[0], optimalScore))
    else:
        print ("The optimal paths are {} with a score of {}".format(optimalPath, optimalScore))

# The optimal path is ['Denver', 'San Diego', 'El Paso', 'Houston', 'Fort Worth', 'San Antonio', 'Austin', 'Dallas', 'Oklahoma City', 'Memphis', 'Indianapolis', 'Columbus', 'Baltimore', 'Washington D.C', 'Boston', 'New York City', 'Philadelphia', 'Louisville', 'Chicago', 'Milwaukee', 'Detroit', 'Nashville', 'Charlotte', 'Jacksonville', 'Phoenix', 'Los Angeles', 'San Jose', 'Portland', 'Seattle', 'San Francisco'] with a score of 11198.849526

