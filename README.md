   What does it do?
    specify:
        which directory to backup
        where to back it up to
        where the HashMap of the previous backup is located
    It creates a HaschMap containing information about the file or folder location and the corresponding hash value.
    then it compares the old HashMap against the newly generated HashMap. It creates a list with update instructions and then                 
    doas the update
    
Options:
    Standard backup => just hit y
    cnb"    =>     create new backup: copys a folder to specified backup location and creates a HashMap
    bse    =>     backup something else: you can tell where to find the HashMap and backupfolder.
    inj     =>     in case some thing went wrong and the HashMap is out of sync with the backupfolder
            It creates a HashMap based on the backup folder, so you have a up-to-date HaschMap
    settings:
        doubbleckeck     creates HashMap of backup directory after the backup is run and compares it against the hashmap generated for the source directory.
        cjf         creates HashMap for directory to backup and backup directory (takes longer to compute)
