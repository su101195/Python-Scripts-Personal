import csv
from datetime import datetime, timedelta
#todo : maps
#https://docs.novatel.com/OEM7/Content/Logs/CLOCKMODEL.htm
header = ['utc','status', 'reject_count', 'propagation_time', 'update_time', 'bias', 'rate', 'Reserved', 'bias_variance', 'covariance', 'Reserved', 'Reserved', 'rate_variance', 'Reserved', 'Reserved', 'Reserved', 'Reserved', 'instantaneous_bias', 'instantaneous_rate', 'Reserved']


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
            
            if line.startswith("<CLOCKMODEL COM4") or line.startswith("[COM4]<CLOCKMODEL COM4"):
                gpsweek = line.split(" ")[5]
                seconds = line.split(" ")[6]

                utc = gpsWeek_seconds_to_datetime(gpsweek, seconds)

                dataline = f.readline()
                dataline = dataline[1:].strip().split(" ")
                

                data.append( tuple([utc] + dataline))
                    
                    
    with open(csvwritepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
