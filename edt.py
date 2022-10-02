import requests
from icalendar import Calendar, Event
from datetime import datetime


class Edt:
    def __init__(self, url: str) -> None:
        response = requests.get(url)
        response = Calendar.from_ical(response.text)
        cours = []
        for component in response.walk():  # copié d'internet mais ça marche donc osef
            if component.name == "VEVENT":
                # Parsing de la description pitié pitié ne changez pas comment est générée la desc
                desc = str(component.get('description')).split("\n")
                # On garde uniquement les valeurs des groupes
                groupes = [i for i in desc if i.startswith("RT")]
                desc = [i for i in desc if i != '' and not i.startswith(
                    "RT") and not i.startswith("(Exporté le:")]  # On vire ce qui sert à rien
                # Le type de cours est tjs le dernier élément (j'éspère)
                typeCours = desc[-1]
                prof = desc[0:-1]

                # Parsing du summary
                summary = str(component.get('summary')).split(" - ")
                if len(summary) == 2:
                    ressource = summary[0]
                    nomRessource = summary[1]
                else:  # nécéssaire pour éviter un crash
                    ressource = summary[0]
                    nomRessource = ""

                cours.append({
                    # on utilise la tz locale
                    'start': component.get('DTSTART').dt.astimezone(),
                    'end': component.get('DTEND').dt.astimezone(),
                    'ressource': ressource,
                    'nomRessource': nomRessource,
                    'typeCours': typeCours,
                    'prof': prof,
                    'groupes': groupes
                })

        self.__edt = sorted(cours, key=lambda i: i['start'])

    # Pour éviter qu'on puisse modifier l'edt
    @property
    def edt(self) -> list:
        return self.__edt

    def getNextNDays(self, n: int = 7) -> list:
        nextNDays = []
        for i in self.__edt:
            # Delta entre les deux dates, permet de choisir les prochains n jours
            delta = i['start'] - datetime.now().astimezone()
            if delta.days < n:
                nextNDays.append(i)
            else:
                # On arrête dès qu'on dépasse la date voulue
                break
        return nextNDays

    # TP, TD ou CM dans les n prochains jours, défaut 7 jours, -1 pour tout
    def getByType(self, type: str, n: int = 7) -> list:
        nextNDays = []

        # Si n=-1 on retourne tout, le delta sera toujours inférieur à 365
        if n == -1:
            n = 365

        for i in self.__edt:
            delta = i['start'] - datetime.now().astimezone()
            if delta.days < n:
                # Pas de "and" pour éviter d'éxécuter le break
                if i['typeCours'] == type:
                    nextNDays.append(i)
            else:
                break
        return nextNDays

    # Cours d'une ressource (forme courte) dans les n prochains jours, défaut 7 jours, -1 pour tout
    def getByRessource(self, ressource: str, n: int = 7) -> list:
        nextNDays = []

        # Si n=-1 on retourne tout, le delta sera toujours inférieur à 365
        if n == -1:
            n = 365

        for i in self.__edt:
            delta = i['start'] - datetime.now().astimezone()
            if delta.days < n:
                # Pas de "and" pour éviter d'éxécuter le break
                if i['ressource'] == ressource:
                    nextNDays.append(i)
            else:
                break
        return nextNDays

    # Cours d'un prof dans les n prochains jours, défaut 7 jours, -1 pour tout
    def getByProf(self, prof: str, n: int = 7) -> list:
        nextNDays = []

        # Si n=-1 on retourne tout, le delta sera toujours inférieur à 365
        if n == -1:
            n = 365

        for i in self.__edt:
            delta = i['start'] - datetime.now().astimezone()
            if delta.days < n:
                # Pas de "and" pour éviter d'éxécuter le break
                if prof in i['prof']:
                    nextNDays.append(i)
            else:
                break
        return nextNDays
