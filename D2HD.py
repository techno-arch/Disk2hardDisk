import wmi
from os import system
#set software and output paths
makemkv = '"C:\Program Files (x86)\MakeMKV\makemkvcon.exe"'
dvddecrypter = '"C:\Program Files (x86)\DVD Decrypter\DVDDecrypter.exe"'
outputpath = r"C:\backup"
#checks to see if a disk is in the drive
raw_wql = "SELECT * FROM __InstanceModificationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_CDROMDrive\'"
c = wmi.WMI()
watcher = c.watch_for(raw_wql=raw_wql)
while 1:
    cd = watcher()
    print(str(cd))#makes debuging easyer for me you can comment it 
    s = "MediaLoaded = TRUE;" in str(cd)#if a disc is in the drive s == true
    if s == True:
        #get drive letter
        drive = max(str(cd).find('Drive = "'), str(cd).find('='), 0)      
        drive = str(cd)[drive:].strip()
        drive = drive.split("\n", 1)[0]
        drive = drive.replace('Drive = "', '')
        drive = drive.replace(':";', '')
        #get space
        disk_space = max(str(cd).find('Size = "'), str(cd).find('='), 0) 
        disk_space = str(cd)[disk_space:].strip()
        disk_space = disk_space.split("\n", 1)[0]
        disk_space = disk_space.replace('Size = "', '')
        disk_space = disk_space.replace('";', '')
        #gets volume serial number
        #there is definently a better way to do this at this point but im lazy 
        serial_number = max(str(cd).find('VolumeSerialNumber = "'), str(cd).find('='), 0) 
        serial_number = str(cd)[serial_number:].strip()
        serial_number = serial_number.split("\n", 1)[0]
        serial_number = serial_number.replace('VolumeSerialNumber = "', '')
        serial_number = serial_number.replace('";', '')
        #if else statment useing the drive_space variable to find out if its a dvd or bluray 
        
        if int(disk_space) >= 9663676416:
               snumb = serial_number in open('bluray').read() 
               if snumb == False:
                 system(r'{} backup --decrypt --cache=16 --noscan -r --progress=-same disc:0 {}/blu-ray'.format(makemkv, outputpath))#backup bluray
                 open('bluray', 'w').write(serial_number + " \n")
        elif int(disk_space) < 9663676415:
               snumb = serial_number in open('dvd').read() 
               if snumb == False:
                 system(r'{} /START /DEST {}/dvd /CLOSE'.format(dvddecrypter, outputpath))#backup disks)
                 open('dvd', 'w').write(serial_number + " \n")
        else: 
            print("error")
            
             
            
