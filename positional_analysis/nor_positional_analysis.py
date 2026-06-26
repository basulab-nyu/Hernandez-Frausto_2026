"""
Jessie - Positional analysis
- accesses a DLC csv file
- compare mouse position to object position at each point in time
- create new columns reporting distance from object and whether mouse is within the object radius (interacting) or not
- generate a new csv file with a list of times when the mouse is in the object radius

Directions:
 - Provide the directory which you will be sourcing the DLC files from
 - Modify the object interactional radius at dis
"""
print("Animal Positional Analysis\nUnits: seconds\n----------")
import csv
import math
import datetime
import os, fnmatch

sessions = []
dis = 75
path = ''

if not os.path.exists(path):
    print(f"Warning: Path '{path}' does not exist.")
else:
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, "*44000.csv"):
                full_path = os.path.join(root, name)
                file_base, _ = os.path.splitext(full_path)
                sessions.append(file_base)
            
for file_name in sessions:
    
    file = open(file_name + '.csv')
    csvreader = csv.reader(file)
    all_rows = []
    interactA = []
    interactB = []
    counter = 0
    for row in csvreader:
        counter += 1
        # update headers for new columns
        if counter == 1:
            row += [row[1],row[1],row[1],row[1],row[1]]
        elif counter == 2:
            row.insert(1, "time")
            row += ["distanceA", "interactA","distanceB","interactB"]
        elif counter == 3:
            row.insert(1, "seconds")
            row += ["distance","Boolean","distance","Boolean"]
        # for each data-containing row,calculate if the mouse head is within 50 pixels of object A or B
        else:
            distanceA = math.sqrt((abs(float(row[1])-float(row[10]))**2)+((abs(float(row[2])-float(row[11])))**2))
            distanceB = math.sqrt((abs(float(row[1])-float(row[13]))**2)+((abs(float(row[2])-float(row[14])))**2))
            row.append(str(distanceA))
            if distanceA <= dis:
                row.append("1")
                interactA.append(1)
            else:
                row.append("0")
                interactA.append(0)
            row.append(str(distanceB))
            if distanceB <= dis:
                row.append("1")
                interactB.append(1)
            else:
                row.append("0")
                interactB.append(0)
            row.insert(1, format((counter - 4) / 66, ".8f"))
        all_rows.append(row)
    file.close()
    # write the updated data to a new file
    newfile = open(file_name + '_analyzed.csv', 'w')
    csvwriter = csv.writer(newfile)
    csvwriter.writerows(all_rows)
    newfile.close()
    # report timestamps when mouse begins and ends object interaction
    counter = 0
    start_rowsA = []
    start_timesA = []
    start_timestampsA = []
    end_rowsA = []
    end_timesA = []
    end_timestampsA = []
    start_rowsB = []
    start_timesB = []
    start_timestampsB =[]
    end_rowsB = []
    end_timesB = []
    end_timestampsB =[]
    for i in range(0, len(interactA)):
        if interactA[i] == 1 and i == 0:
            start_rowsA.append(i)
            start_timesA.append(format(i/66, ".8f"))
            start_timestampsA.append(str(datetime.timedelta(seconds=i//66)))
        elif interactA[i] == 1 and interactA[i-1] == 0:
            start_rowsA.append(i)
            start_timesA.append(format(i/66, ".8f"))
            start_timestampsA.append(str(datetime.timedelta(seconds=i//66)))
        if interactA[i] == 1 and i == (len(interactA)-1):
            end_rowsA.append(i)
            end_timesA.append(format(i/66, ".8f"))
            end_timestampsA.append(str(datetime.timedelta(seconds=i//66)))
        elif interactA[i] == 1 and interactA[i+1] == 0:
            end_rowsA.append(i)
            end_timesA.append(format(i/66, ".8f"))
            end_timestampsA.append(str(datetime.timedelta(seconds=i//66)))
        if interactB[i] == 1 and i == 0:
            start_rowsB.append(i)
            start_timesB.append(format(i/66, ".8f"))
            start_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
        elif interactB[i] == 1 and interactB[i - 1] == 0:
            start_rowsB.append(i)
            start_timesB.append(format(i/66, ".8f"))
            start_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
        if interactB[i] == 1 and i == (len(interactB)-1):
            end_rowsB.append(i)
            end_timesB.append(format(i/66, ".8f"))
            end_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
        elif interactB[i] == 1 and interactB[i + 1] == 0:
            end_rowsB.append(i)
            end_timesB.append(format(i/66, ".8f"))
            end_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
    print(f"Start timestamps (A): {start_timestampsA}")
    'print(f"Start times (A): {start_timesA}")'
    print(f"End timestamps (A):   {end_timestampsA}")
    'print(f"End times (A):   {end_timesA}")'
    print(f"Start timestamps (B): {start_timestampsB}")
    'print(f"Start times (B): {start_timesB}")'
    print(f"End timestamps (B):   {end_timestampsB}")
    'print(f"End times (B):   {end_timesB}")'
    #add interaction times to a new file
    event_file = open(file_name + '_events.csv', 'w')
    csvwriter = csv.writer(event_file)
    csvwriter.writerow(["events","start times A (s)","end times A (s)","start timestamps A (mm:ss)","end timestamps A (mm:ss)","start times B (s)","end times B (s)","start timestamps B (mm:ss)","end timestamps B (mm:ss)"])
    event_number = 0
    if len(start_timesA) > len(start_timesB):
        for i in range(len(start_timesB)):
            event_number += 1
            csvwriter.writerow([event_number,start_timesA[i],end_timesA[i],start_timestampsA[i],end_timestampsA[i],start_timesB[i],end_timesB[i],start_timestampsB[i],end_timestampsB[i]])
        for i in range(len(start_timesB),len(start_timesA)):
            event_number += 1
            csvwriter.writerow([event_number,start_timesA[i],end_timesA[i],start_timestampsA[i],end_timestampsA[i]])
    elif len(start_timesA) < len(start_timesB):
        for i in range(len(start_timesA)):
            event_number += 1
            csvwriter.writerow([event_number,start_timesA[i],end_timesA[i],start_timestampsA[i],end_timestampsA[i],start_timesB[i],end_timesB[i],start_timestampsB[i],end_timestampsB[i]])
        for i in range(len(start_timesA),len(start_timesB)):
            event_number += 1
            csvwriter.writerow([event_number,"","","","",start_timesB[i],end_timesB[i],start_timestampsB[i],end_timestampsB[i]])
    else:
        for i in range(len(start_timesA)):
            event_number += 1
            csvwriter.writerow([event_number, start_timesA[i],end_timesA[i],start_timestampsA[i],end_timestampsA[i],start_timesB[i],end_timesB[i],start_timestampsB[i],end_timestampsB[i]])
    event_file.close()
    #report the length of time the mouse spends interacting with each object
    intervals_A = []
    intervals_B = []
    total_time_A = 0
    total_time_B = 0
    for i in range(0, len(start_timesA)):
        time = float(end_timesA[i])-float(start_timesA[i])
        intervals_A.append(format(time, ".8f"))
        total_time_A += time
    for i in range(0, len(start_timesB)):
        time = float(end_timesB[i])-float(start_timesB[i])
        intervals_B.append(format(time, ".8f"))
        total_time_B += time
    print(f"Interaction Length (A): {intervals_A}")
    print(f"Interaction Length (B): {intervals_B}")
    print(f"Total Time (A): {format(total_time_A, '.8f')}")
    print(f"Total Time (B): {format(total_time_B, '.8f')}")
