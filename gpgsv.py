import csv
#todo : maps
#https://docs.novatel.com/OEM7/Content/Logs/BESTXYZ.htm


#TODO: 
#
params = ["GPGSV"]
header = ['# sat', 'prn', 'elev', 'azimuth', 'SNR']
paramn = 4



def main(logfilepath, csvwritepath, param):
    data = []
    
    #logfilepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/screenlog.00"
    #csvwritepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/bestsats.csv"
    with open(logfilepath, 'r') as f:
        while True: 
            line = f.readline()
            if not line:
                break
            
            if line.startswith(f"${param}") or line.startswith(f"[COM1]${param}"):
                vals = []
                dataline = line.strip().split('*')[0].split(",")[1:]
                assert dataline[1] == str(1), line
                nsat = int(dataline[2])
                
                vals.extend(dataline[3:])
                for i in range(int(dataline[0]) - 1):
                    line = f.readline()
                    dataline = line.strip().split('*')[0].split(",")[1:]
                    
                    #print(dataline[1])
                    #print(str(i+2))
                    assert dataline[1] == str(i+2)

                    
                    assert int(dataline[2]) == int(str(nsat)), dataline[2] + " " + str(nsat)
                    vals.extend(dataline[3:])
                    
                for i in range(nsat):
                    cntstr = ""
                    if i == 0:
                        cntstr = str(nsat)
                    data.append(tuple([cntstr] + vals[i*paramn: i*paramn + paramn ]))
                #fixme nsats string


                    
                    
    with open(csvwritepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
    data.clear()

    
if __name__ == '__main__':
    import os
    for x in params: 
        serials = ["FM - Serial_ DNAR22449330T", "FM - Serial_ DNAR22449353L", "FM - Serial_ DNAR22449442W", "FM - Serial_ DNAR22449187H", "FM - Serial_ DNAR22449366S", "FM - Serial_ DNAR22449432H"]
        path = "Tests Results"
        for serial in serials:
            for session in range(1,3):
                
                
                logfilepath = os.path.join(path, serial, f"Session {session}", "screenlog.00")
                csvwritepath = os.path.join(path, serial, f"Session {session}", "csv")
                if not os.path.exists(csvwritepath):
                    os.makedirs(csvwritepath)
                
                main(logfilepath, os.path.join(csvwritepath, f"{x}.csv"), x)
                print(serial, session, x)
