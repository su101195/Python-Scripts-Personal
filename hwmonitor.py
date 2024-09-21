import csv

#Reference https://docs.novatel.com/OEM7/Content/Logs/HWMONITOR.htm
header = ["Meas_Count", "Source", "Reading", "Error"]
error_map = {
    0x00: "acceptable",
    0x01: "lower warning",
    0x02: "lower error",
    0x03: "upper warning",
    0x04: "upper error",
}
#OEM 7700
reading_type_map = {
    0x00: "Reserved",
    0x01: "Temperature",
    0x02: "Antenna Current",
    0x06: "Digital Core 3V3 Voltage",
    0x07: "Antenna Voltage",
    0x08: "Digital 1V2 Core Voltage",
    0x0F: "Regulated Supply Voltage",
    0x11: "1V8",
    0x15: "5V Voltage (Volts)",
    0x16: "Secondary Temperature",
    0x17: "Peripheral Core Voltage",
    0x18: "Secondary Antenna Current",
    0x19: "Secondary Antenna Voltage",
}


def hex_split(hex_string):
    try:
        # Convert hex to binary and pad with zeros to ensure 16 digits
        binary_string = format(int(hex_string, 16), '016b')
    except ValueError:
        raise ValueError("Invalid hexadecimal input")
    
    if len(binary_string) > 16:
        raise ValueError("Input cannot be fit in 16 binary digits")

    #first number    
    first_number = int(binary_string[-8], 2)
    second_number = int(binary_string[:8], 2)
    
    #assert error_map[first_number] == "acceptable"
    return reading_type_map[second_number], error_map[first_number]




def main(logfilepath, csvwritepath):
    data = []

    
    #logfilepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/screenlog.00"
    #csvwritepath = "/home/ephraim/src/log2csv/Session 3 12 May-20230516T053848Z-001/Session 3_ 12 May/bestsats.csv"
    with open(logfilepath, 'r') as f:
        while True: 
            line = f.readline()
            if not line:
                break
            
            if line.startswith("<HWMONITOR COM1") or line.startswith("[COM1]<HWMONITOR COM1"):
                countline = int(f.readline()[1:].strip()) 
                assert countline == 10
                for i in range(countline):
                    values = f.readline()[1:].strip().split(' ')
                    reading = float(values[0])
                    #print(reading)
                    source, error_msg = hex_split(values[1])
                    countstr = ""
                    if i == 0:
                        countstr = str(countline)
                    #print(source, reading, error_msg)
                    data.append( (countstr, source, reading, error_msg))
                    
                    
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
            
            main(logfilepath, os.path.join(csvwritepath, "HWMONITOR.csv"))
            print(serial, session)
