from ast import arg
import urllib.request
from webbrowser import open as wbopen
from urllib.error import HTTPError as HTTPError
from time import sleep
import os
import argparse
import sqlite3
import ssl

def findAnimeLinkNameLength(animeName, index):
	i=0
	while True:
		if(animeName[index+i].isnumeric() == False):
			return i
		i+=1

def downloadIsNotCompleted():
	for fname in os.listdir("C:\\Users\\manuf\\Downloads"):
		if fname.endswith(".part") or fname.endswith(".crdownload"):
			return 1
	return 0

def findEpNum(animeName):
	cur.execute("SELECT num FROM anime WHERE name=?", (animeName,))
	return int(cur.fetchall()[0][0])

def animeInsert(name):
	num=input("Inserire il numero dell'ultimo episodio scaricato\n")
	link=input("Inserire il link\n")
	cur.execute("INSERT INTO anime (name, num, link) VALUES (?, ?, ?)", (name, num, link))
	db.commit()

db=sqlite3.connect("C:\\Users\\manuf\\anime.db")
cur=db.cursor()

parser=argparse.ArgumentParser()
parser.add_argument('animeName', type=str, help='Nome dell\'anime')
parser.add_argument('epNumber', type=int, help='Numero di episodi')
args=parser.parse_args()

flagDownloadEpNum = False
flagUpdateEpNum = False
if(args.animeName[0] == '.'):
    flagDownloadEpNum = True
    args.animeName = str(args.animeName[1:])

elif(args.animeName[0] == '!'):
    flagDownloadEpNum = True
    flagUpdateEpNum = True
    args.animeName = str(args.animeName[1:])

animeName=args.animeName
numEp=args.epNumber
animeName=animeName.lower()

try:
	cur.execute("SELECT link FROM anime WHERE name=?", (animeName,))
	string=cur.fetchall()[0][0]
except IndexError:
	print("Anime non presente nel database")
	answer=input("Si desidera inserirlo? Y/n ")
	if answer.lower()=="y":
		animeInsert(animeName)
	quit()

epNum=findEpNum(animeName)
if flagDownloadEpNum:
    epNum = numEp
    index=string.find("Ep_")+3
    animeLinkNameLenght=findAnimeLinkNameLength(string, index) 
    epNumStr=str(epNum)
    if(len(epNumStr)==1):
        epNumStr='0'+epNumStr
    string=string[:index] + epNumStr + string[index+animeLinkNameLenght:]
    try:
        context = ssl._create_unverified_context()
        urllib.request.urlopen(string, context=context)
        wbopen(string)
        sleep(5)
        if flagUpdateEpNum:
            cur.execute("UPDATE anime SET num=? WHERE name=?", (epNum, animeName))
            db.commit()
    except HTTPError:
        print("Episodio non esistente o link anime modificato")
        pass
    else:
        while(downloadIsNotCompleted()):
            pass
        print(str(animeName)+"-"+str(epNum), "scaricato correttamente")

else:
	desEpNum=epNum+numEp
	index=string.find("Ep_")+3
	animeLinkNameLenght=findAnimeLinkNameLength(string, index)
	while(epNum<desEpNum):
		epNum+=1
		epNumStr=str(epNum)
		if(len(epNumStr)==1):
			epNumStr='0'+epNumStr
		string=string[:index] + epNumStr + string[index+animeLinkNameLenght:]
		try:
			context = ssl._create_unverified_context()
			urllib.request.urlopen(string, context=context)
			wbopen(string)
			sleep(5)
			cur.execute("UPDATE anime SET num=? WHERE name=?", (epNum, animeName))
			db.commit()
		except HTTPError:
			print("Episodio non esistente o link anime modificato")
			pass
		else:
			while(downloadIsNotCompleted()):
				pass
			print(str(animeName)+"-"+str(epNum), "scaricato correttamente")

if db:
	db.close()
