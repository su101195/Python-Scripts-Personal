import csv
#todo : maps
#https://docs.novatel.com/OEM7/Content/Logs/TIME.htm
header = ['gps reference week', 'gps seconds', 'clock status', 'offset', 'offset std', 'utc offset', 'utc year', 'utc month', 'utc day', 'utc hour', 'utc min', 'utc ms', 'utc status']

def main(logfilepath, csvwritepath):
    data = []

    #logfilepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/screenlog.00"
    #csvwritepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/bestsats.csv"
    with open(logfilepath, 'r') as f:
        while True: 
            line = f.readline()
            if not line:
                break
            
            if line.startswith("<TIME COM4") or line.startswith("[COM4]<TIME COM4"):
                headerline = line
                headerline = headerline.strip().split(" ")
                dataline = f.readline()
                dataline = dataline[1:].strip().split(" ")
                

                data.append( tuple([headerline[5]] + [headerline[6]] + dataline))
                    
                    
    with open(csvwritepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    import os
    serials = ["gps1", "gps21", "gps21_4Hz", "gps3_4Hz"]
    for serial in serials:         
        logfilepath = os.path.join(serial + ".txt")
        csvwritepath = os.path.join(serial)
        if not os.path.exists(csvwritepath):
            os.makedirs(csvwritepath)
        
        main(logfilepath, os.path.join(csvwritepath, "TIME.csv"))
        print(serial)
