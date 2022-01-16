import requests
import json
import sys

from modules.getdata import get_token_id
sys.path.insert(1, 'modules')
from getdata import *

def note():
    n = int(input("Pour quelle période voulez-vous les données ?:\n 0. Le 1er trimestre \n 1. Le relevé du T1 \n 2. Le 2ème trimestre \n 3. Le 3ème trimestre \n 4. Les notes de toute l'année.\n Votre choix ( 0,1,2,3 ou 4) : "))
    print(get_note(n))
    
def devoir():
    print(devoir)

print("Veuillez vous identifiez pour accéder aux fonctions.")
id = input("Entrez votre identifiant : ")
mdp = input("Entrez votre mot de passe : ")
get_token_id(id,mdp)

choix = int(input("Quel informations souhaitez-vous obtenir ?\n 1. Vos notes\n 2.Vos devoirs \n 3.Des informations sur ce logiciel.\n Votre choix ( 1,2 ou 3): "))

if choix == 1:
    note()
if choix == 2:
    devoir()
if choix == 3:
    print("""Ce logiciel fonctionne sur la base d'une API privée et le créateur de cette application ne peut en aucun cas accéder \n à vos données personnelles ( comme l'id, le mdp , vos professeur ...)\n Les fonctionnalité à venir sont l'affichage de la liste des professeurs ou encore l'affichage de l'EDT \net bien plus encore.\n Si vous avez des suggestions,envoyer moi vos idées à cette adresse mail : samsungastuce@gmail.com""")





