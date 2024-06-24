from enum import Enum

class scalefactor(Enum): 
    Normal =1 
    Day = 2
    Month = 3

class Eigenschaften(Enum):
    Eingaenge = 1
    Ausgaenge = 2
    Summe = 3 
    Luftfeuchtigkeit = 4
    Temperatur = 5
    
 

def timescaling(myfile,  sc_factor: scalefactor): 
    try:
        
        lines = []
        groupedDate = {}

        for line in myfile:     
            lines.append(line.strip().split(","))

        for item in lines: 
                date = item[0].split(" ")[0]
                item[0] = date 
        
        if(sc_factor == scalefactor.Month): 
            for el in lines: 
                key = el[0].split("-")[1]

                if key not in groupedDate: 
                    groupedDate[key] = []
                groupedDate[key].append(el)

        if(sc_factor == scalefactor.Day):
            for el in lines: 
                key =  el[0].split("-")[0]+ "-" + el[0].split("-")[1]
                if key not in groupedDate: 
                    groupedDate[key]=[]
                groupedDate[key].append(el)

        if(sc_factor == scalefactor.Normal): 
            groupedDate = myfile

        # for key, group in groupedDate.items(): 
        #         print(f"Group {key}:")
        #         for item in group:
        #             print (item)
        return groupedDate

    except FileNotFoundError:
        print("File not found: 'serial_data.txt'")

# Call the function to execute it

# data = timescaling("day")
# for key, group in data.items():
#     print(f"Group {key}:")
#     for item in group:          
#         print (item)
  

def getAverage(data, whichValue : Eigenschaften):
    averages = {}
    
    for key, group in data.items():
        total_value = 0
        count = 0
        
        for item in group:
            if whichValue == Eigenschaften.Eingaenge:
                value = int(item[1].replace("->", "").strip())
                total_value += value
                count += 1

            if whichValue == Eigenschaften.Ausgaenge:
                value = int(item[2].replace("<-","").strip())
                total_value += value
                count += 1

            if whichValue == Eigenschaften.Summe:
                value = int(item[3].replace("$","").strip())
                total_value += value
                count += 1
            
            # if whichValue == Eigenschaften.Luftfeuchtigkeit:
            #     value = int(item[4].replace("%","").strip())
            #     total_value += value
            #     count += 1

            # if whichValue == Eigenschaften.Temperatur:
            #     value = int(item[5].replace("C","").strip())
            #     total_value += value
            #     count += 1

        if count > 0:
            average_value = total_value / count
            averages[key] = average_value
        else:
            averages[key] = 0

    return averages


def data_lesen():
        # Öffnen der Datei im Lesemodus
        try:
            with open("serial_data.txt", "r") as myfile:
                # Initialisieren einer leeren Liste, um die Zeilen zu speichern
                lines = []
                
                # Durchlaufen jeder Zeile in der Datei
                for line in myfile:
                    # Entfernen des Zeilenumbruchs und Hinzufügen zur Liste
                    lines.append(line.strip())
                
                # Rückgabe der Liste mit den Zeilen
                return lines
        except FileNotFoundError:
            print("Datei 'serial_data.txt' nicht gefunden.")
            return []

# data = timescaling("day")
# averages = getAverage(data, "ein")
# for key, average in averages.items():
#     print(f"Gruppe: {key}, Durchschnittswert: {average}")



def process_average_data(daten):
    zeiten, yeinDaten, yausDaten, yanzMäuser = [], [], [], []
    averagesEin = getAverage(daten, Eigenschaften.Eingaenge)
    averagesAus = getAverage(daten, Eigenschaften.Ausgaenge)
    averageSum = getAverage(daten, Eigenschaften.Summe)
    averageTemp = getAverage(daten, Eigenschaften.Temperatur)
    averageLuft_F = getAverage(daten, Eigenschaften.Luftfeuchtigkeit)

    for key in daten.keys():
        zeiten.append(key)
        yeinDaten.append(averagesEin.get(key, 0))
        yausDaten.append(averagesAus.get(key, 0))
        yanzMäuser.append(averageSum.get(key, 0))
    
    return zeiten, yeinDaten, yausDaten, yanzMäuser