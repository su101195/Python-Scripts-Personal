# Sensor signal mask in hex format
signal_mask_hex = "00000003"
signal_mask = int(signal_mask_hex, 16)

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
    
}

used_solutions = []

for key, value in mask_table.items():
    if key & signal_mask:
        used_solutions.append(value)

#print("Used solutions:", used_solutions)
