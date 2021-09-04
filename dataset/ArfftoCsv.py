# Importing library
import os

# Getting all the arff files from the current directory
files = [arff for arff in os.listdir('.') if arff.endswith(".arff")]

# Function for converting arff list to csv list
def toCsv(text,name):
    data = False
    loop = True
    header = ""
    new_content = []
    # maxData = 5
    i = 1
    no = 1
    splitData = 1
    lengthData = 0
    all_data = False
    labels = ["Normal\n","UDP-Flood\n","Smurf\n","SIDDOS\n","HTTP-FLOOD\n"]
    maxLabelIndex = [200,200,200,200,200]
    countLabelIndex = [0,0,0,0,0]
    boolLabelIndex = [False,False,False,False,False]

    for line in text:
        if not data:
            if "@DATA" in line or "@data" in line:
               data = True
        else:
            lengthData += 1


    data = False
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
                header += '\n'
                new_content.append(header)
        else:
            splitJson = line.split(",")
            if len(splitJson) > 0 :
                label = splitJson[len(splitJson)-1]
                if label in labels:
                    if countLabelIndex[labels.index(label)] == maxLabelIndex[labels.index(label)]:
                        boolLabelIndex[labels.index(label)] = True
                    if not boolLabelIndex[labels.index(label)]:
                        countLabelIndex[labels.index(label)] = countLabelIndex[labels.index(label)]+1
                        new_content.append(line)
                    
                    if all(boolLabelIndex) or i >= lengthData:
                        with open(name + "-split_ke-"+str(splitData)+ ".csv", "w") as outFile:
                            outFile.writelines(new_content)
                            if not all_data:
                                break
                        no = 1
                        splitData += 1
                        new_content = []
                        new_content.append(header)
                    else:
                        no += 1
            
            i += 1
    return new_content


# Main loop for reading and writing files
for file in files:
    with open(file, "r") as inFile:
        content = inFile.readlines()
        name, ext = os.path.splitext(inFile.name)
        toCsv(content, name)