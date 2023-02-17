import requests
import json
import urllib 
from art import *
import matplotlib.pyplot as plt
from getpass4 import getpass

global s
s = requests.Session()
s.headers.update({'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6',
        'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.ecoledirecte.com',
        'referer': 'https://www.ecoledirecte.com/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
})

global token


def connect(username,password):
	payload = '''data={
        "uuid": "",
        "identifiant": "username",
        "motdepasse": "password",
        "isReLogin": false
    }
        '''
	username = urllib.parse.quote(username)
	password = urllib.parse.quote(password)
	payload = payload.replace('username',username).replace('password',password)
	s.headers.update({'content-length':f'{len(payload)}'})
	r = s.post('https://api.ecoledirecte.com/v3/login.awp?v=4.26.3',data=payload)
	
	
	try:
		answer = json.loads(r.text)
		if answer['code'] == 200:
			token = answer['token']
			id_user = answer['data']['accounts'][0]['id']
			write_in_file('id_user.txt',id_user)
			write_in_file('token.txt',token)
			s.headers.update({'x-token':f'{token}'}) 
		else :
			print(answer['message'])
			quit()
	except ValueError as e:
		print(e)



def notes(whatiwant):
	payload = '''data={
    "anneeScolaire": ""
}'''
	s.headers.update({'content-length':f'{len(payload)}'})
	id_user = read_in_file('id_user.txt')
	r = s.post(f'https://api.ecoledirecte.com/v3/Eleves/{id_user}/notes.awp?verbe=get&v=4.27.1',data=payload)
	answer = json.loads(r.text)
	toutelesnotes = answer['data']['notes']

	if whatiwant == 'moyenne_annuelle':
		somme_coef = 0
		somme_notes = 0
		for x in range(0,len(toutelesnotes)):
			#print(toutelesnotes[x]['valeur']+'/'+toutelesnotes[x]['noteSur']+' coef : '+toutelesnotes[x]['coef']+' en '+toutelesnotes[x]['libelleMatiere'])
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False :
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['noteSur'] == 20 :
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True:
				pass
		print("Votre moyenne annuelle est de :",round(somme_notes/somme_coef,2))

	if whatiwant == 'mediane_annuelle':
		notes = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False :
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
			if toutelesnotes[x]['noteSur'] == 20 :
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True:
				pass
		notes.sort()
		if len(notes)%2 == 0:
			mediane = float((notes[int(len(notes)/2)]+notes[int((len(notes)/2)+1)]))/2
		if len(notes)%2 != 0:
			mediane = notes[int((len(notes)+1)/2)]
		print("Votre médiane annuelle est de",round(mediane,2))

	if whatiwant == 'mediane_A001':
		notes = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A001':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A001':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or  toutelesnotes[x]['codePeriode'] != 'A001':
				pass
		notes.sort()
		if len(notes)%2 == 0:
			mediane = float((notes[int(len(notes)/2)]+notes[int((len(notes)/2)+1)]))/2
		if len(notes)%2 != 0:
			mediane = notes[int((len(notes)+1)/2)]
		print("Votre médiane du T1 est de",round(mediane,2))

	if whatiwant == 'mediane_A002':
		notes = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A002':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A002':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or  toutelesnotes[x]['codePeriode'] != 'A002':
				pass
		notes.sort()
		if len(notes)%2 == 0:
			mediane = float((notes[int(len(notes)/2)]+notes[int((len(notes)/2)+1)]))/2
		if len(notes)%2 != 0:
			mediane = notes[int((len(notes)+1)/2)]
		print("Votre médiane du T2 est de",round(mediane,2))




	if whatiwant == 'mediane_A003':
		notes = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A003':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A003':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or  toutelesnotes[x]['codePeriode'] != 'A003':
				pass
		notes.sort()
		if len(notes)%2 == 0:
			mediane = float((notes[int(len(notes)/2)]+notes[int((len(notes)/2)+1)]))/2
		if len(notes)%2 != 0:
			mediane = notes[int((len(notes)+1)/2)]
		print("Votre médiane du T3 est de",round(mediane,2))



	if whatiwant == 'A001':
		somme_coef = 0
		somme_notes = 0
		for x in range(0,len(toutelesnotes)):
			#print(toutelesnotes[x]['valeur']+'/'+toutelesnotes[x]['noteSur']+' coef : '+toutelesnotes[x]['coef']+' en '+toutelesnotes[x]['libelleMatiere'])
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A001':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A001':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['codePeriode'] != 'A001':
				pass
		if somme_notes == 0:
			print("Vous n'avez pas de notes sur la période A001.")
		else:
			print("Votre moyenne pour la période A001 est de :",round(somme_notes/somme_coef,2))
	
	if whatiwant == 'A002':
		somme_coef = 0
		somme_notes = 0
		for x in range(0,len(toutelesnotes)):
			#print(toutelesnotes[x]['valeur']+'/'+toutelesnotes[x]['noteSur']+' coef : '+toutelesnotes[x]['coef']+' en '+toutelesnotes[x]['libelleMatiere'])
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A002':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A002' and toutelesnotes[x]['nonSignificatif'] == False:
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['codePeriode'] != 'A002':
				pass
		if somme_notes == 0:
			print("Vous n'avez pas de notes sur la période A002.")
		else:
			print("Votre moyenne pour la période A002 est de :",round(somme_notes/somme_coef,2))
	

	if whatiwant == 'A003':
		somme_coef = 0
		somme_notes = 0
		for x in range(0,len(toutelesnotes)):
			#print(toutelesnotes[x]['valeur']+'/'+toutelesnotes[x]['noteSur']+' coef : '+toutelesnotes[x]['coef']+' en '+toutelesnotes[x]['libelleMatiere'])
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A003':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A003':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['codePeriode'] != 'A003':
				pass
		if somme_notes == 0:
			print("Vous n'avez pas de notes sur la période A003.")
		else:
			print("Votre moyenne pour la période A003 est de :",round(somme_notes/somme_coef,2))

	if whatiwant == 'tracetoutelesnotes':
		notes = []
		dates = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False :
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['noteSur'] == 20 :
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True:
				pass
		plt.plot(dates,notes)
		plt.xlabel("Date")
		plt.ylabel("Note")
		ax=plt.gca()
		ax.get_xaxis().set_visible(False)
		ax.set_ylim(0, 20)
		plt.title("Tracé annuel des notes")
		plt.show()

	if whatiwant == 'tracenotesA001':
		notes = []
		dates = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A001':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A001':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['codePeriode'] != 'A001':
				pass
		plt.plot(dates,notes)
		plt.xlabel("Date")
		plt.ylabel("Note")
		plt.title("Tracé des notes du T1")
		ax=plt.gca()
		ax.get_xaxis().set_visible(False)
		ax.set_xlim(0, 20)
		plt.show()
	if whatiwant == 'tracenotesA002':
		notes = []
		dates = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A002':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A002':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['codePeriode'] != 'A002':
				pass
		plt.plot(dates,notes)
		plt.xlabel("Date")
		plt.ylabel("Note")
		plt.title("Tracé des notes du T2")
		ax=plt.gca()
		ax.get_xaxis().set_visible(False)
		ax.set_ylim(0, 20)
		plt.show()
	if whatiwant == 'tracenotesA003':
		notes = []
		dates = []
		for x in range(0,len(toutelesnotes)):
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['codePeriode'] == 'A003':
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['codePeriode'] == 'A003':
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))
				notes.append(note)
				dates.append(toutelesnotes[x]['date'])
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['codePeriode'] != 'A003':
				pass
		plt.plot(dates,notes)
		plt.xlabel("Date")
		plt.ylabel("Note")
		plt.title("Tracé des notes du T3")
		ax=plt.gca()
		ax.get_xaxis().set_visible(False)
		ax.set_xlim(0, 20)
		plt.show()

def notes_matieres(matiere,periode):
	payload = '''data={
    "anneeScolaire": ""
}'''
	s.headers.update({'content-length':f'{len(payload)}'})
	id_user = read_in_file('id_user.txt')
	r = s.post(f'https://api.ecoledirecte.com/v3/Eleves/{id_user}/notes.awp?verbe=get&v=4.27.1',data=payload)
	answer = json.loads(r.text)
	toutelesnotes = answer['data']['notes']
	if periode == None:
		somme_coef = 0
		somme_notes = 0
		for x in range(0,len(toutelesnotes)):
			#print(toutelesnotes[x]['valeur']+'/'+toutelesnotes[x]['noteSur']+' coef : '+toutelesnotes[x]['coef']+' en '+toutelesnotes[x]['libelleMatiere'])
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['libelleMatiere'] == matiere:
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['libelleMatiere'] == matiere:
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['libelleMatiere'] != matiere:
				pass
		if somme_notes == 0:
			print("Vous n'avez pas de notes pour la matière : ",matiere)
		else:
			print("Votre moyenne annuelle pour la matière",matiere,"est de :",round(somme_notes/somme_coef,2))
	if periode != None:
		somme_coef = 0
		somme_notes = 0
		for x in range(0,len(toutelesnotes)):
			#print(toutelesnotes[x]['valeur']+'/'+toutelesnotes[x]['noteSur']+' coef : '+toutelesnotes[x]['coef']+' en '+toutelesnotes[x]['libelleMatiere'])
			if toutelesnotes[x]['noteSur'] != 20 and toutelesnotes[x]['valeur'] != 'Abs\xa0' and toutelesnotes[x]['nonSignificatif'] == False and toutelesnotes[x]['libelleMatiere'] == matiere and toutelesnotes[x]['codePeriode'] == periode:
				note = (20*float(toutelesnotes[x]['valeur'].replace(',', '.'))/float(toutelesnotes[x]['noteSur']))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['noteSur'] == 20 and toutelesnotes[x]['libelleMatiere'] == matiere and toutelesnotes[x]['codePeriode'] == periode:
				note = float(toutelesnotes[x]['valeur'].replace(',', '.'))*float(toutelesnotes[x]['coef'])
				somme_coef += float(toutelesnotes[x]['coef'])
				somme_notes += note
			if toutelesnotes[x]['valeur'] == 'Abs\xa0' or toutelesnotes[x]['nonSignificatif'] == True or toutelesnotes[x]['libelleMatiere'] != matiere or toutelesnotes[x]['codePeriode'] != periode:
				pass
		if somme_notes == 0:
			print("Vous n'avez pas de notes pour la matière : ",matiere)
		else:
			print("Votre moyenne pour la période",periode,"pour la matière",matiere,"est de :",round(somme_notes/somme_coef,2))
	





def listes_matieres():
	payload = '''data={
    "anneeScolaire": ""
}'''
	s.headers.update({'content-length':f'{len(payload)}'})
	id_user = read_in_file('id_user.txt')
	r = s.post(f'https://api.ecoledirecte.com/v3/Eleves/{id_user}/notes.awp?verbe=get&v=4.27.1',data=payload)
	answer = json.loads(r.text)
	ensemblematieres = answer['data']['periodes'][0]['ensembleMatieres']['disciplines']
	listes_matieres = []
	for x in range(0,len(ensemblematieres)):
		listes_matieres.append(ensemblematieres[x]['discipline'])
	return listes_matieres




def write_in_file(name,towrite):
	file = open(name,'w')
	file.write(str(towrite))
	file.close()

def read_in_file(name):
	file = open(name,'r')
	read = file.read()
	file.close()
	return read









if __name__ == '__main__':
	tprint("ECOLE   DIRECTE")
	print("Ce logiciel vous permets pour l'instant 4 choses :\n 1. Connaître votre moyenne\n 2. Connaitre votre médiane\n 3. Effectuer le tracé de vos notes\n 4. Les moyennes par matières")
	choix = int(input("Entrer un nombre entre 1 et 4 : "))
	if choix == 1:
		print("Vous avez choisi la moyenne.\nSouhaitez-vous votre :\n 1.Moyenne annuelle\n 2.Moyenne par periode")
		type_moyenne = int(input("Entrer un nombre entre 1 et 2: "))
		if type_moyenne == 1:
			identifiant = input("Votre identifiant : ")
			motdepasse = getpass('Votre mot de passe : ')
			try:
				connect(identifiant,motdepasse)
			except:
				"Vos identifiants sont incorrectes !"
			notes('moyenne_annuelle')
		if type_moyenne == 2:
			print("Vous avez choisi la moyenne par periode.\n 1.Trimestre 1\n 2.Trimestre 2\n 3.Trimestre 3")
			trimestre = int(input("Entrer un nombre entre 1 et 3 : "))
			if trimestre == 1:
				print("Vous avez choisi le premier trimestre.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n ( aucune information ne sera collectée).")
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('A001')
			elif trimestre == 2:
				print("Vous avez choisi le second trimestre.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('A002')
			elif trimestre == 3:
				print("Vous avez choisi le troisième trimestre.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('A003')
	if choix == 2:
		print("Vous avez choisi la médiane.Souhaitez-vous :\n 1. La médiane annuelle\n 2. La médiane par periode")
		type_mediane = int(input("Entrer un nombre entre 1 et 2 : "))
		if type_mediane == 1:
			print("Vous avez choisi la médiane annuelle.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")	
			identifiant = input("Votre identifiant : ")
			motdepasse = getpass('Votre mot de passe : ')
			try:
				connect(identifiant,motdepasse)
			except:
				"Vos identifiants sont incorrectes !"
			notes('mediane_annuelle')
		if type_mediane == 2:
			print("Vous avez choisi la médiane par période. Souhaitez-vous :\n 1. Le trimestre 1\n 2. Le trimestre 2\n 3. Le trimestre 3")
			trimestre_mediane = int(input("Entrer un nombre entre 1 et 3 : "))
			if trimestre_mediane == 1:
				print("Vous avez choisi la médiane pour le trimestre 1.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")	
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('mediane_A001')
			if trimestre_mediane == 2:
				print("Vous avez choisi la médiane pour le trimestre 2.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")	
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('mediane_A002')
			if trimestre_mediane == 3:
				print("Vous avez choisi la médiane pour le trimestre 3.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")	
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('mediane_A003')
	if choix == 3:
		print("Vous avez choisi le tracé de vos notes. Souhaitez-vous\n 1. Le tracé annuel\n 2. Le tracé par periode")
		trace = int(input("Entrer un nombre entre 1 et 2 : "))
		if trace == 1:
			print("Vous avez choisi le tracé annuel de vos notes.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")	
			identifiant = input("Votre identifiant : ")
			motdepasse = getpass('Votre mot de passe : ')
			try:
				connect(identifiant,motdepasse)
			except:
				"Vos identifiants sont incorrectes !"
			notes('tracetoutelesnotes')
		if trace == 2:
			print("Vous avez choisi le tracé par période de vos notes.Souhaitez-vous\n 1. Le premier trimestre\n 2. Le deuxième trimestre\n 3. Le troisième trimestre")	
			periode = int(input("Entrer un nombre entre 1 et 3 : "))
			if periode == 1:
				print("Vous avez choisi le T1.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('tracenotesA001')
			if periode == 2:
				print("Vous avez choisi le T2.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('tracenotesA002')
			if periode == 3:
				print("Vous avez choisi le T3.\n Je vais vous demander d'entrer vos identifiants ECOLE DIRECTE\n(aucune information ne sera collectée).")
				identifiant = input("Votre identifiant : ")
				motdepasse = getpass('Votre mot de passe : ')
				try:
					connect(identifiant,motdepasse)
				except:
					"Vos identifiants sont incorrectes !"
				notes('tracenotesA003')

	if choix == 4:
		print("Vous avez choisi les moyennes par matières.Connectez-vous pour voir la liste de vos matières.")
		identifiant = input("Votre identifiant : ")
		motdepasse = getpass('Votre mot de passe : ')
		try:
			connect(identifiant,motdepasse)
		except:
			"Vos identifiants sont incorrectes !"
		l = listes_matieres()
		counter = 1
		for el in l:
			print(str(counter)+'. '+el)
			counter += 1
		matiere = int(input("Entrer un nombre entre 1 et "+str(counter-1)+' pour sélectionnez la matière : '))
		type_stat = int(input("Souhaitez-vous\n 1. La moyenne annuelle\n 2. La moyenne par période\nEntrer un nombre entre 1 et 2 : "))
		if type_stat == 1:
			notes_matieres(l[matiere-1],None)
		if type_stat !=1 :
			periode = int(input('Vous avez choisi la moyenne par periode.\n 1. 1er trimestre\n 2. 2e trimestre\n 3. 3e trimestre\nEntrer un nombre entre 1 et 3 : '))
			if periode == 1:
				notes_matieres(l[matiere-1],'A001')
			if periode == 2:
				notes_matieres(l[matiere-1],'A002')
			if periode == 3:
				notes_matieres(l[matiere-1],'A003')
