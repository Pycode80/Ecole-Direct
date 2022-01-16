import requests
import json


def get_token_id(id,mdp):
    url = "https://api.ecoledirecte.com/v3/login.awp"

    payload = "data={\n\t\"identifiant\": \""+id+"\",\n\t\"motdepasse\": \""+mdp+"\"\n}"
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    feedback = response.text
    d = json.loads(feedback)
    def get_id():
        data = d.get("data")
        accounts = data.get("accounts")
        liste = accounts[0]
        id = liste.get("id")
        return id    
    file = open("token.txt","w")
    file.write(d.get("token"))
    file.close
    file2 = open("id.txt","w")
    file2.write(str(get_id()))
    file2.close()


def get_note(n):
    token = open("token.txt","r").read()
    id = open("id.txt",'r').read()

    url = "https://api.ecoledirecte.com/v3/eleves/"+id+"/notes.awp?verbe=get"

    payload = "data={\n\t\"token\": \""+token+"\"\n}"
    headers = {}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    feedback = response.text
    d = json.loads(feedback)
    data = d.get("data")
    periodes = data.get("periodes")
    dico = periodes[n] # 5 periodes disponible T1 , releve du T1 , T2, T3, et Année
    ensemble = dico.get("ensembleMatieres")
    nom = dico.get("periode")
    date_fin = dico.get("dateFin")
    moyenne_perso = ensemble.get("moyenneGenerale")
    moyenne_classe = ensemble.get("moyenneClasse")
    moyenne_max = ensemble.get("moyenneMax")
    nom_pp = ensemble.get("nomPP")
    return(f"La periode {nom} se termine le {date_fin}. \nTa moyenne générale est de {moyenne_perso}.\n La moyenne maximum est de {moyenne_max}.\n La moyenne de classe est de {moyenne_classe}.\n Le nom de ton professseur principale est {nom_pp}")
    

def devoir():
    token = open("token.txt","r").read()
    id = open("id.txt",'r').read()
    url = "https://api.ecoledirecte.com/v3/Eleves/"+id+"/cahierdetexte.awp?verbe=get"

    payload = "data={\n\t\"token\": \""+token+"\"\n}"
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    feedback = response.text
    d = json.loads(feedback)
    data = d.get("data")
    count = 0
    for item in data:
        date = data.get(item)
        for x in range(0,len(date)):
            dico = date[x]
            matiere = dico.get("matiere")
            donneLe = dico.get("donneLe")
            interro = dico.get("interrogation")
            print(f"Pour le {item}, il y a des {matiere} à faire. Ces devoirs ont été donnés le {donneLe}. Interrogation : {interro}")
        


