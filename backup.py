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
    def list2(dir, osura, sura, cb):                        # dir dir definition of function which creates filesystem.jason
        data = {}                                           # inizialisiert Dictionerys in which filesystem will be stored
        summe = 0                                           # creates Variable to add file hashes up in order to have directory hash
        directory = os.fsencode(dir)                        # in case a path to file gets passed: fdencode removes the file: b'out/puts/path/like/this'
        for file in os.listdir(directory):                  # for files/folders in do:"
            f = os.path.join(directory, file)               # creates path to file
            fileName= str(file)[2:-1]                       # [2:-1] removes the first tow and last letter, in order to get only filename
            src = str(f)[2:-1]                              # 
            if cb == "c":
                src = src.replace(osura, sura)
            if os.path.isfile(f):                           # if pafh is regular file returns true
                hash = int(calc_hash_file(f), 16)           # aufruf hash funktion
                data[hash] = [fileName, hash, src]          # schreiben von daten in Dictory, dabei ist der key das Hash value der Datei um suchen einfacher zu machen
                summe += hash                               # aufsummieren der hachs der datein im Folder hasch zu berechnen
            else:                                           # hash ist kein regular file → folder
                ret = list2(f, osura, sura, cb)             # rekursives aufrufen der list2 funktion um datein zu erfassem
                summe += ret[1]                             # adding hash keys up
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
    def find_diff(dict1, dict2, dst, dc):                                   # defines function
        # print("start funk")                                               # debugging
        if "hash" in dict1 and dict1.get('hash') != dict2.get('hash'):      # checks if hash of folder is the same 
            #print(dict1.keys())                                            # debigging
            for key in dict1.keys():                                        # für Keys in dict tuhe:
                if type(dict1[key]) is dict and key in dict2:               # wenn key ein dict(folder) ist, und in dict2 vorkommt vergleiche sie
                    print("reloop, checking hash, KEY is:")                 # debugging
                    find_diff(dict1[key], dict2[key], dst, dc)              # recursiv fkt. ruft sich selbst auf
                elif type(dict1[key]) is dict and key not in dict2:         # wenn key ein dict ist aber nicht in dict2 vorkommt 
                    print("folder is missing: " +key)                       # debugging
                    mm = dict1[key]["realpath"]                             # passes mm the realpath value which is by the way the absolutpath
                    mm = mm.replace("/home/lhl", dst)                       # creates absolutpath to file desination replaces /home/ with value of dst
                    print("sink directory: " +mm)                           # debugging
                    diff.append(["Folder", " ", dict1[key]["realpath"], mm, dc])  # schreibe folder path in liste dc delete copy anweisung für update funktion
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

def update(list):                                                   # definition update funktion
    print()
    print("these are the instructions for update():")               # debugging
    print(list)                                                     # debigging
    print()
    faildo = []                                                     # creates list with faild copying atemmpts
    for entry in list:                                              # für einträge in liste tuhe: cycles thrue list
        if entry[4] == "d":                                         # überprüft ob instrucktion als "d" == delete gedacht ist
            if entry[0] == "Folder":                                # überprüft ob listen element einen Ordner darstellt
                if os.path.isdir(entry[3]):                         # verhindert fehlermedung, überprüft ob Ordner in Backup location vorhanden ist 
                    print("deleting Folder from: " +entry[3])       # user
                    shutil.rmtree(entry[3])                         # löscht ordner
                else: 
                    print(entry[3] +" is already deleted")          # user
            else:                                                   # wenn nicht Ordner dann Datei  
                if os.path.isfile(entry[3]):                        # verhindert fehlermedung, überprüft ob Datei in Backup location vorhanden ist
                    print("deleting file from: " +entry[3])         # user
                    os.remove(entry[3])                             # löscht Datei
                else:
                    print(entry[3] + " is already deleted")         # user
        print()
    for entry in list:                                              # cycles thrue list
        if entry[4] == "c":                                         # überprüft ob listen eintrag(instruction) als "c" == copy gedacjt ist
            if entry[0] == "Folder":                                # überprüft ob listen eintrag einen Ordner darstellt
                if os.path.isdir(entry[2]):
                    print("copying Folder from: " +entry[2], " to: " +entry[3])     # user
                    shutil.copytree(entry[2], entry[3])                             # copiert ordner in Ziel 
                else:
                    print(entry[2] +" : Is not proborbly named")
                    faildo.append(entry[2])
            else:                                                                   # wenn kein ordner dann Datei
                if os.path.isfile(entry[2]):
                    print("copying file from: " +entry[2], " to: " +entry[3])       # user
                    pathto = os.path.dirname(entry[3])                              # entfernt filoname.extention von Path
                    shutil.copy2(entry[2], pathto)                                  # copiert Datei an zielort und erhält dabei Metadaten copy anstadt copy2 ohne metadaten
                else:
                    faildo.append(entry[2])
                    print(entry[2] +" : Is not proborbly named")
        print()
    return(faildo)

def pathtest(input_promt, preset):                      # to test is path given by user is valid
    path = ""
    while path == "":
        if preset:                                      # setup value of "path" dependent on wrether preset is True or not
            path = input_promt
        else:                                           # gets user input for required system path
            print(input_promt)
            path = input(input_promt)
        
        if os.path.exists(path):                        # tests if given path is reachable or not
            print(path + " reachable")
        else:
            print(path + " NOT reachable")
            path = ""
            if preset:
                return("ERROR")
    return(path)

def create_json(dstJ, wbackupDJ, wbackupFJ, cb_i):
    if cb_i == "c":                                     # to UPDATE: .json if contents in backup_dir got alterd
        print("creating backup.json for: " + "dst")
        m = list2(dstJ, dstJ, wbackupDJ, cb_i)          # (dir_to_backup), (path_to_replace), (path_to_replace_path_with), c_replace
    
    elif cb_i == "n":                                   # to CREATE: json for dir_to_backup/source/wbackupD
        m = list2(wbackupDJ, " ", " ", "b")             # call to function who makes dir to .json
        #print(t[0])                                    # debugging the [0] thing maks so that only the real json file gets exported otherwise you cant really work with the json sice it hase one {} to much 
       
    with open(wbackupFJ, "w") as f:                     # writes dictionary to json file
        json.dump(m[0], f)                              # m[0] scips the first [] and writes to to the above defined json file
    return("done")



# https://stackoverflow.com/questions/64268575/how-can-i-import-a-json-as-a-dict
#== Main script ================================================================================================
if __name__ == "__main__":
    print()
    again = True
    # backup presets
    preset =[
            ["usb_preset", "/run/media/lhl/71D0-8A5F", "/run/media/lhl/71D0-8A5F/backup.json", "/home/lhl/Documents"],
            ["preset_name", "dst"                    , "(wbackupF) path to .json"            , "(wbackupD) surce"]
            ]

    clollums = len(preset)
    print(clollums)
    while again:
        use_preset = input("use preset [y/N] ")
        
        if use_preset == "y":
            preset_c = True
            count = 0
            which_preset = ""

            print("use: 'q' to exit")
            while which_preset == "":
                rep = input("Use: " + preset[count][0] + " [y/N] ")
                if rep == "y":
                    which_preset = count
                else:
                    count += 1
                if count >= clollums:
                    count = 0
                if rep == "q":
                    which_preset = "exit"
                    use_preset = ""

        if use_preset == "y" and which_preset < clollums:
            print("selected preset: "+ preset[count][0])
            question = preset[count][1]                          # wehre to place the backup
            dst = pathtest(question, preset_c)
            
            question = preset[count][2]                          # wehre to find the backup.json file
            wbackupF = pathtest(question, preset_c) 
            
            question = preset[count][3]                          # what directory to backup
            wbackupD = pathtest(question, preset_c)

            HhHhH = pathtest(dst + "/" + os.path.basename(wbackupD), preset_c)
            
            if HhHhH != "ERROR" and wbackupF == "ERROR":                                                    # if backup.json is not found but backup dir is present. sugesst to create new backup.json
                print("no backup.json found under: " + preset[count][2] + " restoreing ...")
                print(create_json(preset[count][1], preset[count][3], preset[count][2]))
                wbackupF = preset[count][2]
                again = False
                wtd = "bse"
            if wbackupD == "ERROR":
                print("fatal ERROR, cant acess dir to backup: " + preset[count][3])
                again = True
            if HhHhH == "ERROR" and wbackupD != "ERROR" and dst != "ERROR":
                print("backup dir doas not exist. presets are: ")
                print(preset[count][:])
                if "y" == input("initialize preset backup for above settings [y/N]: "):
                    if os.path.exists(preset[count][2]):
                        os.remove(preset[count][2])
                    wbackupF = preset[count][2]
                    again = False
                    #print("wemadeit")
                    wtd = "cnb"
            
            if dst != "ERROR" and wbackupD != "ERROR" and wbackupF != "ERROR" and HhHhH != "ERROR":
                wtd = "bse"
                again = False
        else:
            preset_c = False
            print("Options")                                                                                # Anzeigen der Programm Optionen
            print(" cnb         creates new backup (creates backup.json and copies files)")                 # ↓
            print(" bse         backup someting else (backups to some already existing backup and json)")   # ↓
            print(" inj         creates a backup.json file on a backup directory")                          #
            print(" settings    enters Settings menue")                                                     #
            #print("")                                              # jet to be definde. new default backup settings for diffrent files
            print()
            wtd = input("enter one of the above Options: ")         # abfrage user input
            if wtd == "cnb":
                question = "wehre do you want to have your backup.json located? Input absolut path: you HAVE to call the file backup.json"
                wbackupF = pathtest(question, preset_c) 
                
                question = "what directory do you want to backup. Input absolut path: "
                wbackupD = pathtest(question, preset_c)
                
                question = "where to save the backup. Input absolut path: "
                dst = pathtest(question, preset_c)
                
                again = False

            if wtd == "bse":
                question = "where is your backup.json located. Input absolut path: "
                wbackupF = pathtest(question, preset_c) 
                
                question = "what directory doas this backup refer to? Input absolut path: "
                wbackupD = pathtest(question, preset_c)
                
                question = "where to save the backup. Input absolut path: "
                dst = pathtest(question, preset_c)
                
                again = False

            if wtd == "inj":
                question = "where do you want to have your backup.json located? Input absolut path: "               # /run/media/yourbackupdevice/backup.json
                wbackupF = pathtest(question, preset_c)
                
                question = "give to path to where this backup.json used to copy its files from:"                    # /run/media/YOURBACKUPDEVICE/Documents
                wbackupD = pathtest(question, preset_c)
                
                question = "where is your backup directory located. Input absolut path: "                           # /home/lhl/Documents
                dst = pathtest(question, preset_c)
                
                again = True
                print(create_json(dst, wbackupD, wbackupF, "c"))

            if wtd == "settings":
                enable_dubblecheck = input("do you want to enable doublecheck [y/N]: ")
                enable_cjf = input("do you want to create the backup.json file for the backup dir aswell [y/N]: ")
                if enable_cjf == "y":
                    createjasonOnbackupDir = True
                if enable_dubblecheck == "y":
                    doubblecheck = True

#== loads "old" backup.json
    if createjasonOnbackupDir:                                  # if program is set to create json for backup directory aswell => doas not load the backup.json
        nm = os.path.basename(wbackupD)                         # extracts Directory to backup 
        nm = "/" + nm                                           # adds / to Directory name
        nm = wbackupD.replace(nm, "")                           # rewrites path to backup directory with path to main directory in order to compare
        #nnm = wbackupF.replace("backup.json", "test.json")     # creates new path to backup.json file
        m = list2(wbackupD, dst, nm, "c")                       # (dirto backup), (pathto replace), (path to replace psth with), c replace
        with open(wbackupF, "w") as f:                          # writes dictionary to json file
            json.dump(m[0], f)                                  # t[0] scips the first [] and writes to to the above defined json file
        with open(wbackupF, "r") as m:
            old = json.load(m)
    else:
        if os.path.isfile(wbackupF):                                    # überprüft ob es bereits eine backupdatei gibt
            #print("fdsaasdf")
            nn = wbackupF.replace("backup.json", "oldbackup.json")      # replaces wbackupF with new file name
            os.rename(wbackupF, nn)                                     # renames backup.json to oldbackup.json
            with open(nn, 'r') as file1:                                # opens oldbackup.json
                old = json.load(file1)                                  # writes contents of oldbackup.json to vraiable old

#== creates "new" backup.json meaning: crates a json containing allfiles in specified directory
    print(create_json(dst, wbackupD, wbackupF, "n"))

#== used to create backup on new device
    if wtd == "cnb":                                        # cecs if option create new backup is set
        Folderwo = os.path.basename(wbackupD)               # variable used to create path to backup Directory
        #print(Folderwo)                                    # debugging
        sink = wbackupF.replace("backup.json", Folderwo)    # creates path to backup directory
        inst = [["Folder", "hash", wbackupD, sink, "c"],]   # creates instruction list for update finction
        update(inst)                                        # calls update funktion and passes instruction list
        print("done")                                       # user

#== load new backup.json
    if use_preset == "y" or wtd == "bse":                           # überprüft, ob ein vergleich der backup.json datein gewünscht ist
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
        faildo = update(inst)                               # calls function to dpdate files on backup location returns a list containing files and folders which couldent be updated due to naming issues
        if not faildo:                                      # if faildo list is empty (all files have been updated)
            if doubblecheck:                                # if setting doubbleckeck
                nm = os.path.basename(wbackupD) 
                nm = "/" + nm
                nm = wbackupD.replace(nm, "")
                nnm = wbackupF.replace("backup.json", "test.json")
                m = list2(wbackupD, dst, nm, "c")                   # (dirto backup), (pathto replace), (path to replace psth with), c replace
                with open(nnm, "w") as f:                           # writes dictionary to json file
                    json.dump(m[0], f)                              # t[0] scips the first [] and writes to to the above defined json file
                with open(nnm, "r") as m:
                    test = json.load(m)
                del inst[:]
                val = find_diff(new, test, "", "")
                if not val:
                    print("backup sucessful")
                else:
                    print("it apears that some files, have not been copyed")
                    print("list of missing Files: ")
                    print(val)
            else:                                                   # this will be executed if all goes well
                print("backup sucessful")
        else:                                                       # if faildo is not empty (some files couldent be updated)
            print("backup partialy faild!")
            print("generating backup.json for " + dst)
            os.remove(wbackupF)                                     # delets .json file for update
            dst+= "/" + os.path.basename(wbackupD)                  # creates path to backup directory
            print("igot here")
            # updates reruns .json by creating a .json for backup dir but replacing the filepaths of files listed in .json to match the filepaths to surce(wbackupD)
            print(create_json(dst, wbackupD, wbackupF, "c"))
            
            print("backup failed due to files noit being named proporly")
            print(faildo)                                           # print files which couldent be copied
            print("rename them and run the backup again")
