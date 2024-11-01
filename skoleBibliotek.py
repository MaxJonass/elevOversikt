import tkinter as tk
from tkinter import font
from tkinter import messagebox
import json

with open('liste.json','r',encoding='utf-8') as f:
    data = json.load(f)

root = tk.Tk()
root.title("Elev Oversikt")
root.geometry("500x500")
root.resizable(False,False)


'''
Funksjoner
'''

#For å legge til elev
class nyElev: #Lage en klasse for å definere en ny elev.
    def __init__(self,navn,klasse,programområde):#variabler som er viktige
            
            self.navn = navn  
            self.klasse = klasse
            self.programområde = programområde

    def lagNyElev(self):#funksjon innafor klassen som lager en variabel som kan sendes inn i listen
        elev={
            "navn": self.navn,
            "klasse": self.klasse,
            "programområde": self.programområde,
            "tilgjengelighet": True
        }
        return elev


def leggTil(): #ny funksjon uttafor klassen som skal sende inn den nye eleven
    navn = str(nyElevNavnInput.get()).lower() #henter input fra input feltene i tkinter programmet
    klasse = str(nyElevKlasseInput.get()).upper()
    programområde = str(nyElevProgOmrInput.get()).upper()

    elev = nyElev(navn,klasse,programområde)
    '''bruker klassen ny elev til å generere en elev som skal puttes inn i lista. Vi definerer navn klasse.. med input
    verdiene som er definert over med .get''' 
    elevDict = elev.lagNyElev() #konverterer elev variabelen om til dictionary
    data['elever'].append(elevDict) #bruker append funksjonen for å legge inn i listen.

    with open('liste.json', 'w', encoding='utf-8') as f: #dump data inn i json filen / oppdatere json filen.
        json.dump(data, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Info","Eleven er lagt til") #til slutt en funksjon som gir et popup vindu med beskjed om at eleven er lagt til.



def searchElev():
    value = str(søkEtterElevInput.get()).lower()
    
    
    for sjekk in data['elever']:
        if value == sjekk['navn'] and sjekk['tilgjengelighet'] == False:
              return messagebox.showinfo("Info","Personen går ikke på denne skolen lengre.")

        if value == sjekk['navn'] and sjekk['tilgjengelighet'] == True:
            return messagebox.showinfo("Info", f"Navn: {sjekk['navn']} Klasse: {sjekk['klasse']} Fagområde: {sjekk['programområde']}")
                
        if value != sjekk['navn']:
             return messagebox.showinfo("Info", "Personen er ikke en regristrert elev") 
        


def searchKlasse():
    global root
    global i

    klasseVindu = tk.Toplevel()
    klasseVindu.title("Klasseliste")
    klasseVindu.geometry("500x300")

    textBoks = tk.Text(klasseVindu,height=30, width=80)
    textBoks.grid(row=1)

    value = str(søkEtterKlasseInput.get()).upper()
                 
    for sjekk in data['elever']:
        if sjekk['klasse'] == value and sjekk['tilgjengelighet'] == True:
            textBoks.insert(i,f"Elev Navn: {sjekk['navn']}, Klasse: {sjekk['klasse']}, Programområde: {sjekk['programområde']} \n")
            i+=1
    textBoks['state']='disabled'

    klasseVindu.mainloop()

def fjernElev():
    elevNavn = str(fjernElevNavnInput.get()).lower()
    elevKlasse = str(fjernElevKlasseInput.get()).upper()

    for sjekk in data['elever']:
        if sjekk['navn'] == elevNavn and sjekk['klasse'] == elevKlasse and sjekk['tilgjengelighet'] == False:
              return messagebox.showinfo("Info","Personen går ikke på denne skolen lengre.")

        if elevNavn == sjekk['navn'] and elevKlasse == sjekk['klasse']:

            sjekk['tilgjengelighet']=False

            with open('liste.json', 'w', encoding='utf-8') as f: 
                json.dump(data, f, ensure_ascii=False, indent=4)
            return messagebox.showinfo("Info",f"{elevNavn} er registrert som fjernet.")
            
        elif elevNavn == sjekk['navn'] and elevKlasse != sjekk['klasse']:
             return messagebox.showinfo("Info",f"Vi finner ikke {elevNavn} i klassen {elevKlasse} ")
    return messagebox.showinfo("Info",f"Vi finner ikke {elevNavn} i systemet.")

i=1.0
def vis_elever():
    global root
    global i

    elev_vindu = tk.Toplevel()
    elev_vindu.title("Liste over elever")
    elev_vindu.geometry("500x300")

    tk.Label(elev_vindu, text="Elevliste", font=("Arial", 14)).grid(row=0, column=0, padx=10)
    

    textBoks = tk.Text(elev_vindu,height=30, width=80)
    textBoks.grid(row=1)

    for sjekk in data['elever']:
        if sjekk['tilgjengelighet']==False:
            continue
        textBoks.insert(i,f"Elev Navn: {sjekk['navn']}, Klasse: {sjekk['klasse']}, Programområde: {sjekk['programområde']} \n")
        i+=1
    textBoks['state']='disabled'

    elev_vindu.mainloop()

'''
GUI elementer hoved vindu
'''


tittel = tk.Label(root,text="Elev oversikt", font=font.Font(size=20))
tittel.grid(row=0,column=0)


søkEtterElevLabel = tk.Label(root,text="Søk etter Elev:")
søkEtterElevLabel.grid(row=1,column=0,pady=10)

søkEtterElevInput = tk.Entry(root)
søkEtterElevInput.grid(row=1,column=1,pady=10)

søkEtterElevKnapp = tk.Button(root,text="Søk",command = searchElev)
søkEtterElevKnapp.grid(row=1,column=2,padx=10)


søkEtterKlasseLabel = tk.Label(root,text="Søk etter Klasse")
søkEtterKlasseLabel.grid(row=2,column=0,pady=20)

søkEtterKlasseInput = tk.Entry(root)
søkEtterKlasseInput.grid(row=2,column=1,pady=20)

søkEtterKlasseKnapp = tk.Button(root, text="Søk", command=searchKlasse)
søkEtterKlasseKnapp.grid(row=2,column=2,padx=10)


leggTilElevLabel = tk.Label(root,text="Legg til en ny elev:")
leggTilElevLabel.grid(row=3,column=0)

nyElevNavnLabel = tk.Label(root,text="Skriv inn fullt navn: ")
nyElevNavnLabel.grid(row=4,column=0)

nyElevNavnInput = tk.Entry(root)
nyElevNavnInput.grid(row=4,column=1)

nyElevKlasseLabel = tk.Label(root,text="Skriv Klassen Til Eleven:")
nyElevKlasseLabel.grid(row=5,column=0)

nyElevKlasseInput = tk.Entry(root)
nyElevKlasseInput.grid(row=5,column=1)

nyElevProgOmrLabel = tk.Label(root,text="Skriv inn programområde (REA/SPR):")
nyElevProgOmrLabel.grid(row=6,column=0)

nyElevProgOmrInput = tk.Entry(root)
nyElevProgOmrInput.grid(row=6,column=1)

leggTilElevKnapp = tk.Button(root,text="Legg til elev", command=leggTil)
leggTilElevKnapp.grid(row=7,column=1,pady=10)


fjernElevLabel = tk.Label(root,text="Fjern en elev")
fjernElevLabel.grid(row=8,column=0,pady=10)

fjernElevNavnLabel = tk.Label(root,text="Skriv inn navnet på den du vil fjerne")
fjernElevNavnLabel.grid(row=9,column=0)

fjernElevNavnInput = tk.Entry(root)
fjernElevNavnInput.grid(row=9,column=1)

fjernElevKlasseLabel = tk.Label(root,text="Skriv inn klassen til personen")
fjernElevKlasseLabel.grid(row=10,column=0)

fjernElevKlasseInput = tk.Entry(root)
fjernElevKlasseInput.grid(row=10,column=1)

fjernElevKnapp = tk.Button(root,text="Fjern Elev", command=fjernElev)
fjernElevKnapp.grid(row=11,column=1,pady=10)


visListeOverAlle = tk.Button(root,text="Vis alle Elever på skolen", command=vis_elever)
visListeOverAlle.grid(row=12,column=1,pady=30)

'''
GUI elementer Liste Vindu
'''


root.mainloop()
