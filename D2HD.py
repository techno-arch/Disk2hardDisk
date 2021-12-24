import wmi, shutil
from os import system
makemkv = '"C:\Program Files (x86)\MakeMKV\makemkvcon.exe"'
dvddecrypter = '"C:\Program Files (x86)\DVD Decrypter\DVDDecrypter.exe"'
outputpath = r"F:\backup"

raw_wql = "SELECT * FROM __InstanceModificationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_CDROMDrive\'"
c = wmi.WMI()
watcher = c.watch_for(raw_wql=raw_wql)
while 1:
    cd = watcher()
    open('output.txt', 'w').write(str(cd))
    print(str(cd))
    s = "MediaLoaded = TRUE;" in str(cd)
    if s == True:
    
        drive = max(str(cd).find('Drive = "'), str(cd).find('='), 0)      
        drive = str(cd)[drive:].strip()
        drive = drive.split("\n", 1)[0]
        drive = drive.replace('Drive = "', '')
        drive = drive.replace(':";', '')
        disk_space = max(str(cd).find('Size = "'), str(cd).find('='), 0) 
        disk_space = str(cd)[disk_space:].strip()
        disk_space = disk_space.split("\n", 1)[0]
        disk_space = disk_space.replace('Size = "', '')
        disk_space = disk_space.replace('";', '')
        
        if int(disk_space) >= 9663676416:
            system(r'{} backup --decrypt --cache=16 --noscan -r --progress=-same disc:0 {}/blu-ray'.format(makemkv, outputpath))#backup bluray
            
        elif int(disk_space) < 9663676415:
           system(r'{} /START /DEST {}/dvd /CLOSE'.format(dvddecrypter, outputpath))#backup disks)
         
        else: 
            print("error")
            
            
