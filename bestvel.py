import csv
#todo : maps
#https://docs.novatel.com/OEM7/Content/Logs/BESTVEL.htm
header = ['sol status', 'vel type', 'latency', 'age', 'hor spd', 'trk gnd', 'vert spd', 'Reserved']

def main(logfilepath, csvwritepath):
    data = []
    
    #logfilepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/screenlog.00"
    #csvwritepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/bestsats.csv"
    with open(logfilepath, 'r') as f:
        while True: 
            line = f.readline()
            if not line:
                break
            
            if line.startswith("<BESTVEL COM1") or line.startswith("[COM1]<BESTVEL COM1"):
                dataline = f.readline()
                dataline = dataline[1:].strip().split(" ")
                

                data.append( tuple(dataline))
                    
                    
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
            
            main(logfilepath, os.path.join(csvwritepath, "BESTVEL.csv"))
            print(serial, session)
