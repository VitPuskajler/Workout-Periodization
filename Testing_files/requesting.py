import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.jefit.com/exercises/bodypart.php?id=11&exercises=All&search=&All=0&Bands=0&Bench=1&Dumbbell=1&EZBar=1&Kettlebell=1&MachineStrength=1&MachineCardio=1&Barbell=1&BodyOnly=1&ExerciseBall=0&FoamRoll=0&PullBar=1&WeightPlate=1&Other=0&Strength=1&Stretching=0&Powerlifting=1&OlympicWeightLifting=1&Beginner=0&Intermediate=0&Expert=0&page=1")

soup = BeautifulSoup(page.content, "html.parser")

print(soup)
