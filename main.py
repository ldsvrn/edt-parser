#!/usr/bin/env python3

import requests
import os
from icalendar import Calendar, Event
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')

response = requests.get(url)
response = Calendar.from_ical(response.text)

cours = []
for component in response.walk(): # copié d'internet mais ça marche donc osef
    if component.name == "VEVENT":
        # Parsing de la description pitié pitié ne changez pas comment est générée la desc
        desc = str(component.get('description')).split("\n")
        groupes = [i for i in desc if i.startswith("RT")] # On garde uniquement les valeurs des groupes
        desc = [i for i in desc if i != '' and not i.startswith(
            "RT") and not i.startswith("(Exporté le:")] # On vire ce qui sert à rien
        typeCours = desc[-1] # Le type de cours est tjs le dernier élément (j'éspère)
        prof = desc[0:-1] 

        # Parsing du summary
        summary = str(component.get('summary')).split(" - ")
        if len(summary) == 2:
            ressource = summary[0]
            nomRessource = summary[1]
        else: # nécéssaire pour éviter un crash 
            ressource = summary[0]
            nomRessource = ""

        cours.append({
            'start': component.get('DTSTART').dt.astimezone(), # on utilise la tz locale
            'end': component.get('DTEND').dt.astimezone(),
            'ressource': ressource,
            'nomRessource': nomRessource,
            'typeCours': typeCours,
            'prof': prof,
            'groupes': groupes
        })

cours = sorted(cours, key=lambda i: i['start'])

for i in cours:
    # print(f"{i['start']}: {i['summary']} ({i['typeCours']}, {i['prof']}, {i['groupes']})")
    print(i)
    print("")