import pcpp
import subprocess

#@input Dateipfad der Datei in der die Main liegt
#@return gibt den fertig preprozessierten Code als String zurück
#@Funktionsweise Datei wird geöffnet und gelesen, Präprozessor wird auf den Code ausgeführt,
#neuer Code wird in eine Datei geschrieben welche im selben Ordner liegt wie die Ursprungsdatei,
#Inhalt der neuen Datei wird zurückgegeben
def preProcess(filePath):
    #Öffnen der Ursprungsdatei
    try:
        text = open(filePath).read()
    except:
        print('ERROR: can not read file ' + filePath)
        
    print("Preprocessing...", end="")
    outputFilePath = filePath[:-2] + "_preprocessed.c"
    #Konsolenaufruf für den Präprozessor der den Code in eine neue Datei schreibt
    subprocess.run(["pcpp", filePath, "-o", outputFilePath])
    
    #Öffnen der neuen Datei mit dem bearbeiteten Code
    try:
        processedCCode = open(outputFilePath).read()
    except:
        print("Error: can not open preprocessed C file: " + outputFilePath)

    #Löschen der #line Zeile da diese nur Probleme macht und keine Information für den Compiler liefert
    start = processedCCode.index("#line")
    end = processedCCode[start:].find("\n")
    processedCCode = processedCCode[:start] + processedCCode[start + end :] 

    print("done")


    return processedCCode


    