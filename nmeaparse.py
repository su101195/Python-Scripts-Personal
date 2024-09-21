import csv
#todo : maps
#https://docs.novatel.com/OEM7/Content/Logs/BESTXYZ.htm


#TODO: 
#


params = ["GPGSA", "GNGSA"]
header = {}
header[params[0]] = ['mode MA', 'mode 123'] + 12*['prn'] + ['pdop', 'hdop', 'vdop', 'system ID (only output if the NMEAVERSION is 4.11)']
header[params[1]] = ['mode MA', 'mode 123'] + 12*['prn'] + ['pdop', 'hdop', 'vdop', 'system ID (only output if the NMEAVERSION is 4.11)']




#functions to properly format utc, lat and lon
time_params = ["utc", "lat", "lon"]
def utc(st):
    return f"{st[:2]}:{st[2:4]}:{st[4:]}"

def lat(st):
    return f"{st[:2]}° {st[2:]}'"

def lon(st):
    return f"{st[:3]}° {st[3:]}'"



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
                dataline = line.strip().split('*')[0].split(",")[1:]
                
                for j in time_params:
                    if j in header[param]:
                        dataline[ header[param].index(j) ] = eval( f"{j}(dataline[ header[param].index(j) ])" )
         
                

                data.append( tuple(dataline))
                    
                    
    with open(csvwritepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header[param])
        for row in data:
            writer.writerow(row)
    data.clear()


