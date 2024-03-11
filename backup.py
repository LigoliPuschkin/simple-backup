import os
import hashlib
import json
import shutil
"""
tis code worcks by first creating a  .json file containing ...
"""
doubblecheck = False                                        # set to true if you want to enable double cheking => more computing time
createjasonOnbackupDir = False                              # set to ture if you want to have your backup.json created on backup folder aswell => more computing time
#== hashing =====================================================================================================
if True:
    def calc_hash_file(file_path):                                  # definition of hashing function
        sha256_hash = hashlib.sha256()                              # probably defines hasching algorithem
        with open(file_path, "rb") as file:                         # opens folepath as r(reading/writing)b(binarymode)
            for chunk in iter(lambda: file.read(4096), b""):        # Read the file in chunks of 4096 bytes to handle large files
                sha256_hash.update(chunk)                           # mixes chunks together
        return sha256_hash.hexdigest()                              # returns hash as hex

#== create filesystem jason =====================================================================================
if True:
    def list2(dir, osura, sura, cb):                                         # definition of function which creates filesystem.jason
        data = {}                                           # inizialisiert Dictionerys in which filesystem will be stored
        summe = 0                                           # creates Variable to add file hashes up in order to have directory hash
        directory = os.fsencode(dir)                        # variable to use in order to loop thrue filesystem # writes encodet path/dir
        for file in os.listdir(directory):                  # Return a list containing the names of the entries in the directory given by path. "for files/folders in do:" 
            f = os.path.join(directory, file)               # bastelt aus directory und file name einen absoluten pfad zusammen
            fileName= str(file)[2:-1]                       # [2:-1] entvernt die ersten 2 und den letzten Buchstaben OPTIMIERUNG
            src = str(f)[2:-1]                              # [11:-1] bastelt den relatieven Pfad der Datein zusammen OPTIMIERUNG
            if cb == "c":
                src = src.replace(osura, sura)
            if os.path.isfile(f):                           # if pafh is regular file returns true
                hash = int(calc_hash_file(f),16)            # aufruf hash funktion
                data[hash] = [fileName, hash, src]          # schreiben von daten in Dictory, dabei ist der key das Hash value der Datei um suchen einfacher zu machen
                summe += hash                               # aufsummieren der hachs der datein im Folder hasch zu berechnen
            else:                                           # hash ist kein regular file → folder
                ret = list2(f, osura, sura, cb)                              # rekursives aufrufen der lirsrcst2 funktion um datein zu erfassem
                summe += ret[1]                             # ausummiern der hash key
                data[fileName]= ret[0]                      # ??

        data["hash"] = summe                                # schreibt hash-value des Ordners 
        dirpath = str(directory)[2:-1]                      # entfernen von einzelen zeichen um dir path zu beckommen
        data["realpath"] = dirpath                          # optimieren: return f bze. relpath

        return (data, summe)                                # returns data(Dictionary) ans summe(hash vale for folders)

# https://stackoverflow.com/questions/51753809/accessing-nested-keys-in-python
# https://stackoverflow.com/questions/48652762/how-to-compare-nested-dicts
# https://datagy.io/python-check-if-key-value-dictionary/
# compare old vs. new and new vs. old filesystem ===============================================================
diff = []
if True:
    def find_diff(dict1, dict2, dst, dc):                                            # defines function
        # print("start funk")                                                 # debugging
        if "hash" in dict1 and dict1.get('hash') !=  dict2.get('hash'):     # checks if hach of folder is the same 
            #print(dict1.keys())                                            # debigging
            for key in dict1.keys():                                        # für Keys in dict tuhe:
                if type(dict1[key]) is dict and key in dict2:               # wenn key ein dict(folder) ist, und in dict2 vorkommt vergleiche sie
                    print("reloop, checking hash, KEY is:")                 # debugging
                    find_diff(dict1[key], dict2[key], dst, dc)              # recursiv fkt. ruft sich selbst auf
                elif type(dict1[key]) is dict and key not in dict2:         # wenn key ein dict ist aber nicht in dict2 vorkommt 
                    print("folder is missing: " +key)                       # debugging
                    mm = dict1[key]["realpath"]                             # passes mm the realpath value which is by the way the absolutpath
                    mm = mm.replace("/home/lhl", dst)             # creates absolutpath to file desination replaces /home/ with value of dst
                    print("sink directory: " +mm)                           # debugging
                    diff.append(["Folder" , " ", dict1[key]["realpath"], mm, dc])  # schreibe folder path in liste dc delete copy anweisung für update funktion
                else:                                                       # wenn dict kein dict enthält(datei) vergleiche deren listen(Datein)
                    if key not in dict2:                                    # vergleicht keys = file hash value wenn key nicht in dict2 hat sich datei geändert
                        print("this is else key:" +key)                     # debugging
                        mm = dict1[key][2]                                  # passes mm the absolutpath to file
                        mm = mm.replace("/home/lhl", dst)                   # creates absolut path to file destination
                        print("this is sink directory : " +mm)              # debugging
                        dict1[key].append(mm)                               # hangt path to file destination an liste an
                        dict1[key].append(dc)                               # hängt dc(delete/copy) anweisung für update in liste an
                        diff.append((dict1[key]))                           # schreibt key value(liste) in update liste
        return (diff)                                                       # gibt update list zurück

def update(list):                                                           # definition update funktion
    print()
    print("these are the instructions for update():")                       # debugging
    print(list)                                                             # debigging
    print()
    faildo = []                                                             # creates list with faild copying atemmpts
    for entry in list:                                                      # für einträge in liste tuhe: cycles thrue list
        if entry[4] == "d":                                                 # überprüft ob instrucktion als "d" == delete gedacht ist
            if entry[0] == "Folder":                                        # überprüft ob listen element einen Ordner darstellt
                if os.path.isdir(entry[3]):                                  # verhindert fehlermedung, überprüft ob Ordner in Backup location vorhanden ist 
                    print("deleting Folder from: " +entry[3])               # user
                    shutil.rmtree(entry[3])                                 # löscht ordner
                else: 
                    print(entry[3] +" is already deleted")                  # user
            else:                                                           # wenn nicht Ordner dann Datei
                if os.path.isfile(entry[3]):                                 # verhindert fehlermedung, überprüft ob Datei in Backup location vorhanden ist
                    print("deleting file from: " +entry[3])                 # user
                    os.remove(entry[3])                                     # löscht Datei
                else:
                    print(entry[3] + " is already deleted")                 # user
        print()
    for entry in list:                                                      # cycles thrue list
        if entry[4] == "c":                                                 # überprüft ob listen eintrag(instruction) als "c" == copy gedacjt ist
            if entry[0] == "Folder":                                        # überprüft ob listen eintrag einen Ordner darstellt
                if os.path.isdir(entry[2]):
                    print("copying Folder from: " +entry[2], " to: " +entry[3]) # user
                    shutil.copytree(entry[2], entry[3])                         # copiert ordner in Ziel 
                else:
                    print(entry[2] +" : Is not proborbly named")
                    faildo.append(entry[2])
            else:                                                           # wenn kein ordner dann Datei
                if os.path.isfile(entry[2]):
                    print("copying file from: " +entry[2], " to: " +entry[3])   # user
                    pathto = os.path.dirname(entry[3])                          # entfernt filoname.extention von Path
                    shutil.copy2(entry[2], pathto)                              # copiert Datei an zielort und erhält dabei Metadaten copy anstadt copy2 ohne metadaten
                else:
                    faildo.append(entry[2])
                    print(entry[2] +" : Is not proborbly named")
        print()
    return(faildo)

# https://stackoverflow.com/questions/64268575/how-can-i-import-a-json-as-a-dict
#== Main script ================================================================================================
if __name__ == "__main__":
#== user Input section 
    
    print()
    again = True
    while again:
        backup = input("backup to usb? [y/N] ")
        if backup == "y":
            dst = "/run/media/lhl/71D0-8A5F"                        # wehre to place the backup
            wbackupF = "/run/media/lhl/71D0-8A5F/backup.json"       # wehre to find the backup.json file
            wbackupD = "/home/lhl/Documents"                        # what directory to backup
            wtd = "bse"                                             # sets Option presented to user
            again = False
        else:
            print("Options")                                                                                # Anzeigen der Programm Optionen
            print(" cnb         creates new backup (creates backup.json and copies files)")                 # ↓
            print(" bse         backup someting else (backups to some already existing backup and json)")   # ↓
            print(" inj         creates a backup.json file on a backup directory")                          #
            print(" settings    enters Settings menue")                                                     #
            #print("")                                              # jet to be definde. new default backup settings for diffrent files
            print()
            wtd = input("enter one of the above Options: ")         # abfrage user input
            if wtd == "cnb":
                wbackupF = input("wehre do you want to have your backup.json located? Input absolut path: you HAVE to call the file backup.json")
                wbackupD = input("what directory do you want to backup. Input absolut path: ")
                again = False
            if wtd == "bse":
                wbackupF = input("wehre is your backup.json located. Input absolut path: ")
                wbackupD = input("what directory doas this backup refer to? Input absolut path: ")
                again = False
            if wtd == "inj":
                wbackupF = input("wehre do you want to have your backup.json located? Input absolut path: ")         # /run/media/yourbackupdevice/backup.json
                wbackupD = input("wehre is your backup directory located. Input absolut path: ")                    # /run/media/YOURBACKUPDEVICE/Documents
                wdotbrt  = input("give to path to where this backup.json used to copy its files from: ")             # /home/lhl/Documents
                again = False
            if wtd == "settings":
                enable_dubblecheck = input("do you want to enable doublecheck [y/N]: ")
                enable_cjf = input("do you want to create the backup.json file for the backup dir aswell [y/N]: ")
                if enable_cjf == "y":
                    createjasonOnbackupDir == True
                if enable_dubblecheck == "y":
                    doubblecheck = True


#== loads "old" backup.json
    if createjasonOnbackupDir:                                  # if program is set to create json for backup directory aswell => doas not load the backup.json
        nm = os.path.basename(wbackupD)                         # extracts Directory to backup 
        nm = "/"+nm                                             # adds / to Directory name
        nm = wbackupD.replace(nm, "")                           # rewrites path to backup directory with path to main directory in order to compare
        #nnm = wbackupF.replace("backup.json", "test.json")      # creates new path to backup.json file
        m = list2(wbackupD, dst, nm, "c")                       # (dirto backup), (pathto replace), (path to replace psth with), c replace
        with open(wbackupF, "w") as f:                               # writes dictionary to json file
            json.dump(m[0], f)                                  # t[0] scips the first [] and writes to to the above defined json file
        with open(wbackupF, "r") as m:
            old = json.load(m)
    else:
        if os.path.isfile(wbackupF):                                # überprüft ob es bereits eine backupdatei gibt
            nn = wbackupF.replace("backup.json", "oldbackup.json")      # replaces wbackupF with new file name
            os.rename(wbackupF, nn)                                     # renames backup.json to oldbackup.json
            with open(nn, 'r') as file1:                                # opens oldbackup.json
                old = json.load(file1)                                  # writes contents of oldbackup.json to vraiable old

#== creates "new" backup.json meaning: crates a json containing allfiles in specified directory
    if wtd != "inj":                                # führt diesen schritt immer aus, außer in Optionen ist "inj" augewählt
        t = list2(wbackupD, " ", " ", "b")          # aufrufen der funktion, welche das aktuellen stand des zu backupenden filesystem in .json file umwandelt
        #print(t[0])                                # debugging the [0] thing maks so that only the real json file gets exported otherwise you cant really work with the json sice it hase one {} to much 
        with open(wbackupF, "w") as f:              # writes dictionary to json file
            json.dump(t[0], f)                      # t[0] scips the first [] and writes to to the above defined json file

#== used to create backup on new device
    if wtd == "cnb":                                        # cecs if option create new backup is set
        Folderwo = os.path.basename(wbackupD)               # variable used to create path to backup Directory
        #print(Folderwo)                                     # debugging
        sink = wbackupF.replace("backup.json", Folderwo)    # creates path to backup directory
        inst = [["Folder", "hash", wbackupD, sink, "c"],]   # creates instruction list for update finction
        update(inst)                                        # calls update funktion and passes instruction list
        print("done")                                       # user

#== used if currentstate of backup directory has changed relative to its backup.json file
    if wtd == "inj":                                        # überprüft ob option "inj" gesetzt wurde
        m = list2(wbackupD, wbackupD, wdotbrt, "c")         # (dirto backup), (pathto replace), (path to replace psth with), c replace
        with open(wbackupF, "w") as f:                      # writes dictionary to json file
            json.dump(m[0], f)                              # t[0] scips the first [] and writes to to the above defined json file

#== load new backup.json
    if backup == "y" or wtd == "bse":                               # überprüft, ob ein vergleich der backup.json datein gewünscht ist
        with open(wbackupF, 'r') as file2:                          # opens "new" fliesystem.json
            new = json.load(file2)                                  # saves it as new in order to compare 
        print()
        print("comparing backup.json for updated files and folders")
        print()
        inst = find_diff(new, old, dst, "c")                # compares .json for old files, and writs them along with update instructions in list 
        print()
        print("comparing backup.json for deleted files and folders")
        inst = find_diff(old, new, dst, "d")                # compares .json for old files, and writs them along with update instructions in list
        print("updating backup")                            # user
        faildo = update(inst)                               # calls function to delete files
        if not faildo:
            if doubblecheck:
                nm = os.path.basename(wbackupD)
                nm = "/"+nm
                nm = wbackupD.replace(nm, "")
                nnm = wbackupF.replace("backup.json", "test.json")
                m = list2(wbackupD, dst, nm, "c")         # (dirto backup), (pathto replace), (path to replace psth with), c replace
                with open(nnm, "w") as f:                      # writes dictionary to json file
                    json.dump(m[0], f)                              # t[0] scips the first [] and writes to to the above defined json file
                with open(nnm, "r") as m:
                    test = json.load(m)
                del inst [:]
                val = find_diff(new, test, "", "")
                if not val:
                    print("backup sucessful")
                else:
                    print("it apears that some files, have not been copyed")
                    print("list of missing Files: ")
                    print(val)
            else:
                print("backup sucessful")
        else:
            print("backup faild! please rename the below listed files and backup again")
            os.remove(wbackupF)
            os.rename(nn, wbackupF)
            print(faildo)
