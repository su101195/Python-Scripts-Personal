import csv
from datetime import datetime, timedelta
#https://docs.novatel.com/OEM7/Content/Logs/BESTSATS.htm
header = ['utc','#sats', 'System', 'Satellite ID', 'Status', 'Solution used']


def sigmask(gpstype, signal_mask):
    signal_mask = int(signal_mask, 16)
    sol = ""
    gpsmasks = {
    "GPS": 
            {0x01: "L1",
            0x02: "L2",
            0x04: "L5",},
    "GLONASS": 
            {0x01: "L1",
            0x02: "L2",
            0x04: "L3",},
    "Galileo": 
            {0x01: "E1",
            0x02: "E5A",
            0x04: "E5B",
            0x08: "ALTBOC",
            0x10: "E6",},
    "BeiDou": 
            {0x01: "B1I",
            0x02: "B2I",
            0x04: "B3",
            0x08: "B1C",
            0x10: "B2a",
            0x20: "B2b",},
    "QZSS": 
            {0x01: "L1",
            0x02: "L2",
            0x04: "L5",
            0x08: "L6",},
    "NavIC": 
            {0x04: "L5",},
    # "SBAS": 
    #         {0x0: "NOT USED",},
    
    
    }
    
    for key, value in gpsmasks[gpstype].items():
        if key & signal_mask:
            sol+=f"{value}+"

    
    
    
    return sol[:-1]

def gpsWeek_seconds_to_datetime(gpsweek, seconds):
    gpsweek = int(gpsweek)
    seconds = float(seconds)
    # Number of seconds that have passed since the start of the GPS epoch
    gps_epoch = datetime(1980, 1, 6, 0, 0, 0)
    elapsed_seconds = gpsweek * 7 * 24 * 60 * 60 + seconds
    # Convert to timedelta
    elapsed_seconds -= 18
    delta = timedelta(seconds=elapsed_seconds)
    # Add timedelta to the start of the GPS epoch
    return str(gps_epoch + delta)


def main(logfilepath, csvwritepath):
    data = []
    linecount = 0
    
    #logfilepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/screenlog.00"
    #csvwritepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/bestsats.csv"
    with open(logfilepath, 'r') as f:
        while True: 
            line = f.readline()
            linecount+=1
            if not line:
                break
            
            if line.startswith("<BESTSATS COM4") or line.startswith("[COM4]<BESTSATS COM4"):
                gpsweek = line.split(" ")[5]
                seconds = line.split(" ")[6]

                utc = gpsWeek_seconds_to_datetime(gpsweek,seconds)

                countline = int(f.readline()[1:].strip()) 
                linecount+=1

                
                #assert countline == 39, f"expected {39} but got {countline}" number of sats is not constant
                for i in range(countline):
                    countstr = ""
                    if i == 0:
                        countstr = str(countline)

                
                    
                    dataline = f.readline()
                    linecount+=1
                    dataline =dataline[1:].strip().split(" ")
                    
                    #unmask solutions used
                    #print(linecount)
                    #print(logfilepath)
                    dataline[3] = sigmask(dataline[0], dataline[2])
                    
                    #print(dataline)

                    data.append(tuple([utc] + [countstr] + dataline))
                    
                   
    #print(data) 
    with open(csvwritepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
            

        
if __name__ == '__main__':
    import os
    serials = ["FM - Serial_ DNAR22449330T", "FM - Serial_ DNAR22449353L", "FM - Serial_ DNAR22449442W", "FM - Serial_ DNAR22449187H", "FM - Serial_ DNAR22449366S", "FM - Serial_ DNAR22449432H"]
    path = "Tests Results"
    for serial in serials:
        for session in range(1,3):
            
            
            logfilepath = os.path.join(path, serial, f"Session {session}", "screenlog.00")
            csvwritepath = os.path.join(path, serial, f"Session {session}", "csv")
            if not os.path.exists(csvwritepath):
                os.makedirs(csvwritepath)
            
            main(logfilepath, os.path.join(csvwritepath, "BESTSATS.csv"))
            print(serial, session)
        


#