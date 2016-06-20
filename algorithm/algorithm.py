import random
from collections import defaultdict
import copy
import math

cities = {"New York City": {"lat": 40.7128, "long": 74.0059}, "Los Angeles": {"lat": 34.0522, "long": 118.2437},
          "Chicago": {"lat": 41.8781, "long": 87.6298}, "Houston": {"lat": 29.7604, "long": 95.3698},
          "Philadelphia": {"lat": 39.9526, "long": 75.1652},
          "Phoenix": {"lat": 33.4484, "long": 112.0740}, "San Antonio": {"lat": 29.4241, "long": 98.4936},
          "San Diego": {"lat": 32.7157, "long": 117.1611},
          "Dallas": {"lat": 32.7767, "long": 96.7970}, "San Jose": {"lat": 37.3382, "long": 121.8863},
          "Austin": {"lat": 30.2672, "long": 97.7431},
          "Jacksonville": {"lat": 30.3322, "long": 81.6557}, "Indianapolis": {"lat": 39.7684, "long": 86.1581},
          "San Francisco": {"lat": 37.7749, "long": 122.4194}
    , "Columbus": {"lat": 39.9612, "long": 82.9988}, "Fort Worth": {"lat": 32.7555, "long": 97.3308},
          "Charlotte": {"lat": 35.2271, "long": 80.8431},
          "Detroit": {"lat": 42.3314, "long": 83.0458}, "El Paso": {"lat": 31.7619, "long": 106.4850},
          "Memphis": {"lat": 35.1495, "long": 90.0490},
          "Boston": {"lat": 42.3601, "long": 71.0589}, "Seattle": {"lat": 47.6062, "long": 122.3321},
          "Denver": {"lat": 39.7392, "long": 104.9903},
          "Washington D.C": {"lat": 38.9072, "long": 77.0369}, "Nashville": {"lat": 36.1627, "long": 86.7816},
          "Baltimore": {"lat": 39.2904, "long": 76.6122},
          "Louisville": {"lat": 38.2527, "long": 85.7585}, "Portland": {"lat": 45.5231, "long": 122.6765},
          "Oklahoma City": {"lat": 35.0078, "long": 97.0929},
          "Milwaukee": {"lat": 43.0389, "long": 87.9065}}

paths = []
optimal = []
optimalScore = float("inf")


# This function is based on http://andrew.hedges.name/experiments/haversine/
def calculateDistanceBetweenTwo(city1, city2):
    longs = math.radians(cities[city2]["long"] - cities[city1]["long"])
    lats = math.radians(cities[city2]["lat"] - cities[city1]["lat"])
    lat1 = math.radians(cities[city1]["lat"])
    lat2 = math.radians(cities[city2]["lat"])

    a = math.sin(lats / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(longs / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 3961 * c
    return distance


def initialize():
    i = 0;
    while i < 500:
        path = []
        while len(path) < len(cities.keys()):
            choice = random.choice(cities.keys())
            if choice not in path:
                path.append(choice)
        paths.append(path)
        i += 1;
    return


def scorePortion(path, start, end):
    score = 0
    for i in range(start, end):
        score += calculateDistanceBetweenTwo(path[i], path[i + 1])
    return score


def score(path):
    score = 0;
    for i in range(len(path) - 1):
        score += calculateDistanceBetweenTwo(path[i], path[i + 1])
    return score


def scoreAll(paths):
    scores = defaultdict(list)
    for path in paths:
        scores[score(path)].append(path)
    return scores

def createNextGen():
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
    remaining = []
    for i in range(len(otherParent)):
        if otherParent[i] not in section:
            remaining.append(otherParent[i])

    return remaining


def insertCities(start, section, remainingCities):
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
    mutation = random.random()
    if mutation < 0.10:
        position = random.randint(0, len(child) - 2)
        temp = child[position]
        child[position] = child[position + 1]
        child[position + 1] = temp
    return child


def runsimulation(times):
    global paths
    global optimalScore
    global optimalPath
    for i in range(times):
        nextGen = createNextGen()
        paths = copy.deepcopy(nextGen)
    return


def findOptima(scores):
    topScore = min(scores)
    topPath = scores[topScore]
    if optimalScore < topScore:
        return (optimalScore, optimalPath)
    else:
        return (topScore, topPath)


def main():
    initialize()
    runsimulation(1000)
    scores = scoreAll(paths)
    optimalScore, optimalPath = findOptima(scores)
    if len(optimalPath) is 1:
        print ("The optimal path is {} with a score of {}".format(optimalPath[0], optimalScore))
    else:
        print ("The optimal paths are {} with a score of {}".format(optimalPath, optimalScore))
    return

main()

# The optimal path is ['Denver', 'San Diego', 'El Paso', 'Houston', 'Fort Worth', 'San Antonio', 'Austin', 'Dallas', 'Oklahoma City', 'Memphis', 'Indianapolis', 'Columbus', 'Baltimore', 'Washington D.C', 'Boston', 'New York City', 'Philadelphia', 'Louisville', 'Chicago', 'Milwaukee', 'Detroit', 'Nashville', 'Charlotte', 'Jacksonville', 'Phoenix', 'Los Angeles', 'San Jose', 'Portland', 'Seattle', 'San Francisco'] with a score of 11198.849526

