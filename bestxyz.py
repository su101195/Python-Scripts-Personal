import csv
#todo : maps
#https://docs.novatel.com/OEM7/Content/Logs/BESTXYZ.htm
header = ['utc', 'P-sol status', 'pos type', 'P-X', 'P-Y', 'P-Z', 'P-X sigma', 'P-Y sigma', 'P-Z sigma', 'V-sol status', 'vel type', 'V-X', 'V-Y', 'V-Z', 'V-X sigma', 'V-Y sigma', 'V-Z sigma', 'stn ID', 'V-latency', 'diff_age', 'sol_age', '#SVs', '#solnSVs', '#ggL1', '#solnMultiSVs', 'Reserved', 'ext sol stat', 'Galileo and BeiDou sig mask', 'GPS and GLONASS sig mask']

def ch_tr_status_parse(hex_string):
    pass


def sigmask(signal_mask1, signal_mask2):
    signal_mask1 = int(signal_mask1, 16)
    signal_mask2 = int(signal_mask2, 16)
    sol1 = ""
    sol2 = ""
    
    
    galileobeidou = {
            0x01: "Galileo E1",
            0x02: "Galileo E5a",
            0x04: "Galileo E5b",
            0x08: "Galileo ALTBOC",
            0x10: "BeiDou B1",
            0x20: "BeiDou B2",
            0x40: "BeiDou B3",
            0x80: "Galileo E6",}
        
    gpsglonass = { 
            0x01: "GPS L1",
            0x02: "GPS L2",
            0x04: "GPS L5",
            0x08: "reserved",
            0x10: "GLONASS L1",
            0x20: "GLONASS L2",
            0x40: "GLONASS L3",
            0x80: "reserved",}

    
    for key, value in galileobeidou.items():
        if key & signal_mask1:
            sol1+=f"{value}+"
            
    for key, value in gpsglonass.items():
        if key & signal_mask2:
            sol2+=f"{value}+"
            

    return [sol1[:-1], sol2[:-1] ]
from datetime import datetime, timedelta


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
    with open(logfilepath, 'r') as f:
        while True: 
            line = f.readline()
            if not line:
                break
            
            if line.startswith("<BESTXYZ COM4") or line.startswith("[COM4]<BESTXYZ COM4"):
                gpsweek = line.split(" ")[5]
                seconds = line.split(" ")[6]


                                # Define the start of the GPS epoch

                
                utc = gpsWeek_seconds_to_datetime(gpsweek, seconds)
                


                dataline = f.readline()
                dataline = dataline[1:].strip().split(" ")
                dataline[-2], dataline[-1] = sigmask(dataline[-2], dataline[-1])

                data.append( tuple([utc] + dataline))
                    
                    
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
        for session in range(2,3):
            
            
            logfilepath = os.path.join(path, serial, f"Session {session}", "screenlog.00")
            csvwritepath = os.path.join(path, serial, f"Session {session}", "csv")
            if not os.path.exists(csvwritepath):
                os.makedirs(csvwritepath)
            
            main(logfilepath, os.path.join(csvwritepath, "BESTXYZ.csv"))
            print(serial, session)
