import csv
import json


# def csv_to_json(csvFilePath, jsonFilePath):
#     jsonArray = []
#     fieldnames = ("t","Px_ECI","Py_ECI","Pz_ECI","Vx_ECI","Vy_ECI","Vz_ECI")
      
#     #read csv file
#     with open(csvFilePath, encoding='utf-8') as csvf: 
#         #load csv file data using csv library's dictionary reader
#         csvReader = csv.DictReader(csvf,fieldnames) 

#         #convert each csv row into python dict
#         for row in csvReader: 
#             #add this python dict to json array
#             jsonArray.append(row)
  
#     #convert python jsonArray to JSON String and write to file
#     with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
#         jsonString = json.dumps(jsonArray, indent=4)
#         jsonf.write(jsonString)
          
# csvFilePath = r'Satellite_Ephemeris_True_Data_Epoch_10ms.csv'
# jsonFilePath = r'test.json'
# csv_to_json(csvFilePath, jsonFilePath)

# Step 1: Initialize a Python List
data_list = []

# Step 2 & 3: Read lines of CSV file and convert each line into a dictionary, adding it to the list
with open('Satellite_Ephemeris_True_Data_Epoch_10ms.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Specify which entries to convert to string
        for key, value in row.items():
            if key in ['t']:  # Add column names you want to convert to string here
                row[key] = str(value)
        data_list.append(row)

# Step 4: Convert the Python List to JSON String
json_string = json.dumps(data_list, indent=4)

# Step 5: Write JSON String to a JSON file
with open('test.json', mode='w') as json_file:
    json_file.write(json_string)