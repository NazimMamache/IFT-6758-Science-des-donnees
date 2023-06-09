import json
import pandas as pd


def count_labels(labels: str) -> int:
    """
    Étant donné une chaine de charactères d'étiquettes non traitées, retourne le nombre d'étiquettes distinctes.

    Par exemple:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> 3
    """
    return labels.count(',')+1


def convert_id(ID: str) -> str:
    """
    Créez une fonction qui prend un ID d'étiquette (par exemple "/m/09x0r") et renvoie le nom d'étiquette correspondant (par exemple "Speech")

    Pour ce faire, utilisez la bibliothèque `json` et le fichier `data/ontology.json`, une description du fichier peut être trouvée
    sur https://github.com/audioset/ontology

    Même si lire le fichier à chaque fois et parcourir les éléments pour trouver une correspondance fonctionne assez bien dans notres cas.
    Pensez à des moyens d'accélérer ce processus si, par exemple, cette fonction devait être exécutée 100 000 fois.
    """
    with open('data/ontology.json') as file:
        data = json.load(file)
    file.close()
    return list(filter(lambda x:x["id"]==ID,data))[0]['name']


def convert_ids(labels: str) -> str:
    """
    À l'aide de get_label_name(), créez une fonction qui prend les colonnes d'étiquettes (c'est-à-dire une chaîne de charactères d'ID d'étiquettes séparées par des virgules)
    et renvoie une chaîne de noms d'étiquettes, séparés par des tubes "|".

    Par exemple:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> "Musique|Skateboard|Discours"
    """
    s = ''
    for x in labels.split(','):
        s += convert_id(x) + '|'
    s = s[:-1]
    return s


def contains_label(labels: pd.Series, label: str) -> pd.Series:
    """
    Créez une fonction qui prend une pandas Series de chaînes de charactères où chaque chaîne de charactères est formatée comme ci-dessus
    (c'est-à-dire "|" sépare les noms d'étiquettes comme "Music|Skateboard|Speech") et renvoie une pandas Series avec juste
    les valeurs qui incluent `label`.

    Par exemple, étant donné le label "Music" et la série suivante :
    "Music|Skateboard|Speech"
    "Voice|Speech"
    "Music|Piano"

    la fonction devrait retourner
    "Music|Skateboard|Speech"
    "Music|Piano"
    """
    list = []
    for i in labels.index:
        if label not in labels[i].split("|"):
            list.append(i)
    return labels.drop(list)


def get_correlation(labels: pd.Series, label_1: str, label_2: str) -> float:
    """
    Créez une fonction qui, avec une pandas Series comme décrit ci-dessus, renvoie la proportion de rangées
    avec label_1 qui ont également label_2. Utilisez la fonction que vous avez créée ci-dessus.

    Par exemple, supposons que la pandas Series comporte 1 000 valeurs, dont 120 ont label_1. Si 30 des 120
    ont label_2, votre fonction doit renvoyer 0,25.
    """
    series_1 = contains_label(labels, label_1).reset_index(drop = True)
    series_2 = contains_label(series_1, label_2)

    return len(series_2) / len(series_1)



if __name__ == "__main__":
    print(count_labels("/m/04rlf,/m/06_fw,/m/09x0r"))
    print(convert_id("/m/04rlf"))
    print(convert_ids("/m/04rlf,/m/06_fw,/m/09x0r"))

    series = pd.Series([
        "Music|Skateboard|Speech",
        "Voice|Speech",
        "Music|Piano"
    ])

    print(contains_label(series, "Music"))
    print(get_correlation(series, "Music", "Piano"))
