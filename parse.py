import timep
import clockmodel
import gpgsv
import nmeaparse

import rxstatus
import range2
import bestxyz
import bestsats



import os
str_path = "data/Novatel_FM_01_Log4"
serials = [str_path]
for serial in serials:         
    logfilepath = os.path.join(serial + ".txt")
    csvwritepath = os.path.join(serial)
    if not os.path.exists(csvwritepath):
        os.makedirs(csvwritepath)
    
    timep.main(logfilepath, os.path.join(csvwritepath, "TIME.csv"))
    clockmodel.main(logfilepath, os.path.join(csvwritepath, "CLOCKMODEL.csv"))
    # bestsats.main(logfilepath, os.path.join(csvwritepath, "BESTSATS.csv"))
    print(serial)
    
    
    
serials = [str_path]
for serial in serials:         
    logfilepath = os.path.join(serial + ".txt")
    csvwritepath = os.path.join(serial)
    if not os.path.exists(csvwritepath):
        os.makedirs(csvwritepath)
        
    nmea = ["GPGSA", "GNGSA"]
    for param in nmea:
        nmeaparse.main(logfilepath, os.path.join(csvwritepath, f"{param}.csv"), param)
        
    
        
    range2.main(logfilepath, os.path.join(csvwritepath, "RANGE.csv"))
    bestxyz.main(logfilepath, os.path.join(csvwritepath, "BESTXYZ.csv"))
    bestsats.main(logfilepath, os.path.join(csvwritepath, "BESTSATS.csv"))

        

    
        
    
        
    
    
    


        
    
    
    
    
