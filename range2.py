import csv
from datetime import datetime, timedelta
#https://docs.novatel.com/OEM7/Content/Logs/RANGE.htm
header = ['utc','# obs', 'PRN/slot', 'glofreq', 'psr', 'psr sigma', 'adr', 'adr sigma', 'dopp', 'C/No', 'locktime', 'ch-tr-status']


ch_tr_status = {"Tracking state":(0,4),
                "SV channel number":(5,9),
                "Phase lock flag":(10,10),
                "Parity known flag":(11,11),
                "Code locked flag":(12,12),
                "Correlator type":(13,15),
                "Satellite system":(16,18),
                "Reserved":(19,19), 
                "Grouping":(20,20),
                "Signal type":(21,25),
                "Reserved":(26,26),
                "Primary L1 channel":(27,27),
                "Carrier phase measurement":(28,28),
                "Digital filtering on signal":(29,29),
                "PRN lock flag":(30,30), 
                "Channel assignment":(31,31), }
    
def ch_status(hex_string, counter):
    try:
        # Convert hex to binary and pad with zeros to ensure 16 digits
        binary_string = format(int(hex_string, 16), '032b')
    except ValueError:
        raise ValueError("Invalid hexadecimal input")
    
    if len(binary_string) > 32:
        raise ValueError("Input cannot be fit in 32 binary digits")
    #binary_string = binary_string[::-1]
    vals = []
    for ranges in ch_tr_status.values():
        if "-" in binary_string:
            print(binary_string)
            print(hex_string)
            print(counter)
        vals.append(    int( binary_string[ranges[0]: ranges[1]+1],2))
        
    return vals


header = header + list(ch_tr_status.keys())

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

    
    #logfilepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/screenlog.00"
    #csvwritepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/bestsats.csv"
    counter=0
    with open(logfilepath, 'r') as f:
        while True: 
            line = f.readline()
            counter+=1
            if not line:
                break
            
            if line.startswith("<RANGE COM4") or line.startswith("[COM4]<RANGE COM4"):
                gpsweek = line.split(" ")[5]
                seconds = line.split(" ")[6]

                utc = gpsWeek_seconds_to_datetime(gpsweek,seconds)


                countline = int(f.readline()[1:].strip()) 
                counter+=1
                for i in range(countline):
                    countstr = ""
                    if i == 0:
                        countstr = str(countline)
                    dataline = f.readline()
                    counter+=1
                    dataline = [countstr] + dataline[1:].strip().split(" ")
                    #print(dataline)
                    dataline.extend(ch_status(dataline[-1], counter))
                    data.append(tuple([utc] + dataline))
                    
                   
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
            
            main(logfilepath, os.path.join(csvwritepath, "RANGE.csv"))
            print(serial, session)
    

