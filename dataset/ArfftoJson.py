# Importing library
import os
import json

# Getting all the arff files from the current directory
files = [arff for arff in os.listdir('.') if arff.endswith(".arff")]

# Function for converting arff list to csv list
def toJson(text,name):
    data = False
    header = ""
    json_data = []

    maxData = 5000
    i = 0
    no = 0
    splitData = 1
    lengthData = 0
    all_data = False

    for line in text:
        if not data:
            if "@DATA" in line or "@data" in line:
               data = True
        else:
            lengthData += 1


    for line in text:
        if not data:
            if "@ATTRIBUTE" in line or "@attribute" in line:
                attributes = line.split()
                if("@attribute" in line):
                    attri_case = "@attribute"
                else:
                    attri_case = "@ATTRIBUTE"
                column_name = attributes[attributes.index(attri_case) + 1]
                header = header + column_name + ","
            elif "@DATA" in line or "@data" in line:
                data = True
                header = header[:-1]
                header = header.split(",")
        else:
            splitJson = line.split(",")
            if len(splitJson) > 0:
                data = {}
                index = 0
                for key in header:
                    data[key] = splitJson[index]
                    index += 1
        
                if data:
                    json_data.append(data)
                    
                if no >= maxData or i >= lengthData:
                    print(str(no) +" >= " + str(maxData) +" or "+str(i)+" >= "+ str(lengthData))
                    print(name + "-split_ke-"+str(splitData)+ ".json")
                    with open(name + "-split_ke-"+str(splitData)+ ".json", "w") as outFile:
                        json.dump(json_data, outFile)
                        if not all_data:
                            break
                    no = 1
                    splitData += 1
                    json_data = []   

            no += 1
            i += 1

           
    return json_data


# Main loop for reading and writing files
for file in files:
    with open(file, "r") as inFile:
        content = inFile.readlines()
        name, ext = os.path.splitext(inFile.name)
        toJson(content,name)
        