"""
Positional analysis
- accesses a DLC csv file
- compare mouse position to all hole positions at each point in time
- create new columns reporting distance from object and whether mouse is within a hole's radius (interacting) or not
- generate a new csv file with a list of times when the mouse is in each hole's radius

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
dis = 70
path = '' # change to your actual path

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
    interact_escape, interactB, interactC, interactD, interactE, interactF, interactG, interactH, interactI, interactJ, interactK, interactL, interactM, interactN, interactO, interactP, interactQ, interactR, interactS, interactT = ([] for i in range(20))
    counter = 0
    for row in csvreader:
        counter += 1
        # update headers for new columns (time, distances, and Boolean checks)
        if counter == 1:
            row += [row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1],row[1]]
        elif counter == 2:
            row.insert(1, "time")
            row += ["distance_escape", "interact_escape","distanceB","interactB","distanceC","interactC","distanceD","interactD","distanceE","interactE","distanceF","interactF","distanceG","interactG","distanceH","interactH","distanceI","interactI","distanceJ","interactJ","distanceK","interactK","distanceL","interactL","distanceM","interactM","distanceN","interactN","distanceO","interactO","distanceP","interactP","distanceQ","interactQ","distanceR","interactR","distanceS","interactS","distanceT","interactT"]
        elif counter == 3:
            row.insert(1, "seconds")
            row += ["distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean","distance","Boolean"]
        # for each data-containing row, check if the mouse head is within dis pixels each hole
        else:
            distance_escape = math.sqrt((abs(float(row[1]) - float(row[7])) ** 2) + ((abs(float(row[2]) - float(row[8]))) ** 2))
            distanceB = math.sqrt((abs(float(row[1]) - float(row[10])) ** 2) + ((abs(float(row[2]) - float(row[11]))) ** 2))
            distanceC = math.sqrt((abs(float(row[1]) - float(row[13])) ** 2) + ((abs(float(row[2]) - float(row[14]))) ** 2))
            distanceD = math.sqrt((abs(float(row[1]) - float(row[16])) ** 2) + ((abs(float(row[2]) - float(row[17]))) ** 2))
            distanceE = math.sqrt((abs(float(row[1]) - float(row[19])) ** 2) + ((abs(float(row[2]) - float(row[20]))) ** 2))
            distanceF = math.sqrt((abs(float(row[1]) - float(row[22])) ** 2) + ((abs(float(row[2]) - float(row[23]))) ** 2))
            distanceG = math.sqrt((abs(float(row[1]) - float(row[25])) ** 2) + ((abs(float(row[2]) - float(row[26]))) ** 2))
            distanceH = math.sqrt((abs(float(row[1]) - float(row[28])) ** 2) + ((abs(float(row[2]) - float(row[29]))) ** 2))
            distanceI = math.sqrt((abs(float(row[1]) - float(row[31])) ** 2) + ((abs(float(row[2]) - float(row[32]))) ** 2))
            distanceJ = math.sqrt((abs(float(row[1]) - float(row[34])) ** 2) + ((abs(float(row[2]) - float(row[35]))) ** 2))
            distanceK = math.sqrt((abs(float(row[1]) - float(row[37])) ** 2) + ((abs(float(row[2]) - float(row[38]))) ** 2))
            distanceL = math.sqrt((abs(float(row[1]) - float(row[40])) ** 2) + ((abs(float(row[2]) - float(row[41]))) ** 2))
            distanceM = math.sqrt((abs(float(row[1]) - float(row[43])) ** 2) + ((abs(float(row[2]) - float(row[44]))) ** 2))
            distanceN = math.sqrt((abs(float(row[1]) - float(row[46])) ** 2) + ((abs(float(row[2]) - float(row[47]))) ** 2))
            distanceO = math.sqrt((abs(float(row[1]) - float(row[49])) ** 2) + ((abs(float(row[2]) - float(row[50]))) ** 2))
            distanceP = math.sqrt((abs(float(row[1]) - float(row[52])) ** 2) + ((abs(float(row[2]) - float(row[53]))) ** 2))
            distanceQ = math.sqrt((abs(float(row[1]) - float(row[55])) ** 2) + ((abs(float(row[2]) - float(row[56]))) ** 2))
            distanceR = math.sqrt((abs(float(row[1]) - float(row[58])) ** 2) + ((abs(float(row[2]) - float(row[59]))) ** 2))
            distanceS = math.sqrt((abs(float(row[1]) - float(row[61])) ** 2) + ((abs(float(row[2]) - float(row[62]))) ** 2))
            distanceT = math.sqrt((abs(float(row[1]) - float(row[64])) ** 2) + ((abs(float(row[2]) - float(row[65]))) ** 2))
            
            
            # add the distances and Boolean check to the row
            row.append(str(distance_escape))
            if distance_escape <= dis:
                row.append("1")
                interact_escape.append(1)
            else:
                row.append("0")
                interact_escape.append(0)
            row.append(str(distanceB))
            if distanceB <= dis:
                row.append("1")
                interactB.append(1)
            else:
                row.append("0")
                interactB.append(0)
            row.append(str(distanceC))
            if distanceC <= dis:
                row.append("1")
                interactC.append(1)
            else:
                row.append("0")
                interactC.append(0)
            row.append(str(distanceD))
            if distanceD <= dis:
                row.append("1")
                interactD.append(1)
            else:
                row.append("0")
                interactD.append(0)
            row.append(str(distanceE))
            if distanceE <= dis:
                row.append("1")
                interactE.append(1)
            else:
                row.append("0")
                interactE.append(0)
            row.append(str(distanceF))
            if distanceF <= dis:
                row.append("1")
                interactF.append(1)
            else:
                row.append("0")
                interactF.append(0)
            row.append(str(distanceG))
            if distanceG <= dis:
                row.append("1")
                interactG.append(1)
            else:
                row.append("0")
                interactG.append(0)
            row.append(str(distanceH))
            if distanceH <= dis:
                row.append("1")
                interactH.append(1)
            else:
                row.append("0")
                interactH.append(0)
            row.append(str(distanceI))
            if distanceI <= dis:
                row.append("1")
                interactI.append(1)
            else:
                row.append("0")
                interactI.append(0)
            row.append(str(distanceJ))
            if distanceJ <= dis:
                row.append("1")
                interactJ.append(1)
            else:
                row.append("0")
                interactJ.append(0)
            row.append(str(distanceK))
            if distanceK <= dis:
                row.append("1")
                interactK.append(1)
            else:
                row.append("0")
                interactK.append(0)
            row.append(str(distanceL))
            if distanceL <= dis:
                row.append("1")
                interactL.append(1)
            else:
                row.append("0")
                interactL.append(0)
            row.append(str(distanceM))
            if distanceM <= dis:
                row.append("1")
                interactM.append(1)
            else:
                row.append("0")
                interactM.append(0)
            row.append(str(distanceN))
            if distanceN <= dis:
                row.append("1")
                interactN.append(1)
            else:
                row.append("0")
                interactN.append(0)
            row.append(str(distanceO))
            if distanceO <= dis:
                row.append("1")
                interactO.append(1)
            else:
                row.append("0")
                interactO.append(0)
            row.append(str(distanceP))
            if distanceP <= dis:
                row.append("1")
                interactP.append(1)
            else:
                row.append("0")
                interactP.append(0)
            row.append(str(distanceQ))
            if distanceQ <= dis:
                row.append("1")
                interactQ.append(1)
            else:
                row.append("0")
                interactQ.append(0)
            row.append(str(distanceR))
            if distanceR <= dis:
                row.append("1")
                interactR.append(1)
            else:
                row.append("0")
                interactR.append(0)
            row.append(str(distanceS))
            if distanceS <= dis:
                row.append("1")
                interactS.append(1)
            else:
                row.append("0")
                interactS.append(0)
            row.append(str(distanceT))
            if distanceT <= dis:
                row.append("1")
                interactT.append(1)
            else:
                row.append("0")
                interactT.append(0)
            row.insert(1, format((counter - 4) / 66, ".8f"))
        all_rows.append(row)
    file.close()
    # write the updated data to a new file
    newfile = open(file_name + '_analyzed.csv', 'w')
    csvwriter = csv.writer(newfile)
    csvwriter.writerows(all_rows)
    newfile.close()
    # find times when mouse begins and ends object interaction
    counter = 0
    start_times_escape, start_timestamps_escape, end_times_escape, end_timestamps_escape = ([] for i in range(4))
    start_timesB, start_timestampsB, end_timesB, end_timestampsB = ([] for i in range(4))
    start_timesC, start_timestampsC, end_timesC, end_timestampsC = ([] for i in range(4))
    start_timesD, start_timestampsD, end_timesD, end_timestampsD = ([] for i in range(4))
    start_timesE, start_timestampsE, end_timesE, end_timestampsE = ([] for i in range(4))
    start_timesF, start_timestampsF, end_timesF, end_timestampsF = ([] for i in range(4))
    start_timesG, start_timestampsG, end_timesG, end_timestampsG = ([] for i in range(4))
    start_timesH, start_timestampsH, end_timesH, end_timestampsH = ([] for i in range(4))
    start_timesI, start_timestampsI, end_timesI, end_timestampsI = ([] for i in range(4))
    start_timesJ, start_timestampsJ, end_timesJ, end_timestampsJ = ([] for i in range(4))
    start_timesK, start_timestampsK, end_timesK, end_timestampsK = ([] for i in range(4))
    start_timesL, start_timestampsL, end_timesL, end_timestampsL = ([] for i in range(4))
    start_timesM, start_timestampsM, end_timesM, end_timestampsM = ([] for i in range(4))
    start_timesN, start_timestampsN, end_timesN, end_timestampsN = ([] for i in range(4))
    start_timesO, start_timestampsO, end_timesO, end_timestampsO = ([] for i in range(4))
    start_timesP, start_timestampsP, end_timesP, end_timestampsP = ([] for i in range(4))
    start_timesQ, start_timestampsQ, end_timesQ, end_timestampsQ = ([] for i in range(4))
    start_timesR, start_timestampsR, end_timesR, end_timestampsR = ([] for i in range(4))
    start_timesS, start_timestampsS, end_timesS, end_timestampsS = ([] for i in range(4))
    start_timesT, start_timestampsT, end_timesT, end_timestampsT = ([] for i in range(4))
    for i in range(0, len(interact_escape)):
        # escape hole interactions
        if interact_escape[i] == 1 and i == 0:
            start_times_escape.append(format(i/66, ".8f"))
            start_timestamps_escape.append(str(datetime.timedelta(seconds=i//66)))
        elif interact_escape[i] == 1 and interact_escape[i-1] == 0:
            start_times_escape.append(format(i/66, ".8f"))
            start_timestamps_escape.append(str(datetime.timedelta(seconds=i//66)))
        if interact_escape[i] == 1 and i == (len(interact_escape)-1):
            end_times_escape.append(format(i/66, ".8f"))
            end_timestamps_escape.append(str(datetime.timedelta(seconds=i//66)))
        elif interact_escape[i] == 1 and interact_escape[i+1] == 0:
            end_times_escape.append(format(i/66, ".8f"))
            end_timestamps_escape.append(str(datetime.timedelta(seconds=i//66)))
        # hole B interactions
        if interactB[i] == 1 and i == 0:
            start_timesB.append(format(i/66, ".8f"))
            start_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
        elif interactB[i] == 1 and interactB[i - 1] == 0:
            start_timesB.append(format(i/66, ".8f"))
            start_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
        if interactB[i] == 1 and i == (len(interactB)-1):
            end_timesB.append(format(i/66, ".8f"))
            end_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
        elif interactB[i] == 1 and interactB[i + 1] == 0:
            end_timesB.append(format(i/66, ".8f"))
            end_timestampsB.append(str(datetime.timedelta(seconds=i//66)))
        # hole C interactions
        if interactC[i] == 1 and i == 0:
            start_timesC.append(format(i/66, ".8f"))
            start_timestampsC.append(str(datetime.timedelta(seconds=i//66)))
        elif interactC[i] == 1 and interactC[i - 1] == 0:
            start_timesC.append(format(i/66, ".8f"))
            start_timestampsC.append(str(datetime.timedelta(seconds=i//66)))
        if interactC[i] == 1 and i == (len(interactC)-1):
            end_timesC.append(format(i/66, ".8f"))
            end_timestampsC.append(str(datetime.timedelta(seconds=i//66)))
        elif interactC[i] == 1 and interactC[i + 1] == 0:
            end_timesC.append(format(i/66, ".8f"))
            end_timestampsC.append(str(datetime.timedelta(seconds=i//66)))
        # hole D interactions
        if interactD[i] == 1 and i == 0:
            start_timesD.append(format(i/66, ".8f"))
            start_timestampsD.append(str(datetime.timedelta(seconds=i//66)))
        elif interactD[i] == 1 and interactD[i - 1] == 0:
            start_timesD.append(format(i/66, ".8f"))
            start_timestampsD.append(str(datetime.timedelta(seconds=i//66)))
        if interactD[i] == 1 and i == (len(interactD)-1):
            end_timesD.append(format(i/66, ".8f"))
            end_timestampsD.append(str(datetime.timedelta(seconds=i//66)))
        elif interactD[i] == 1 and interactD[i + 1] == 0:
            end_timesD.append(format(i/66, ".8f"))
            end_timestampsD.append(str(datetime.timedelta(seconds=i//66)))
        # hole E interactions
        if interactE[i] == 1 and i == 0:
            start_timesE.append(format(i/66, ".8f"))
            start_timestampsE.append(str(datetime.timedelta(seconds=i//66)))
        elif interactE[i] == 1 and interactE[i - 1] == 0:
            start_timesE.append(format(i/66, ".8f"))
            start_timestampsE.append(str(datetime.timedelta(seconds=i//66)))
        if interactE[i] == 1 and i == (len(interactE)-1):
            end_timesE.append(format(i/66, ".8f"))
            end_timestampsE.append(str(datetime.timedelta(seconds=i//66)))
        elif interactE[i] == 1 and interactE[i + 1] == 0:
            end_timesE.append(format(i/66, ".8f"))
            end_timestampsE.append(str(datetime.timedelta(seconds=i//66)))
        # hole F interactions
        if interactF[i] == 1 and i == 0:
            start_timesF.append(format(i/66, ".8f"))
            start_timestampsF.append(str(datetime.timedelta(seconds=i//66)))
        elif interactF[i] == 1 and interactF[i - 1] == 0:
            start_timesF.append(format(i/66, ".8f"))
            start_timestampsF.append(str(datetime.timedelta(seconds=i//66)))
        if interactF[i] == 1 and i == (len(interactF)-1):
            end_timesF.append(format(i/66, ".8f"))
            end_timestampsF.append(str(datetime.timedelta(seconds=i//66)))
        elif interactF[i] == 1 and interactF[i + 1] == 0:
            end_timesF.append(format(i/66, ".8f"))
            end_timestampsF.append(str(datetime.timedelta(seconds=i//66)))
        # hole G interactions
        if interactG[i] == 1 and i == 0:
            start_timesG.append(format(i/66, ".8f"))
            start_timestampsG.append(str(datetime.timedelta(seconds=i//66)))
        elif interactG[i] == 1 and interactG[i - 1] == 0:
            start_timesG.append(format(i/66, ".8f"))
            start_timestampsG.append(str(datetime.timedelta(seconds=i//66)))
        if interactG[i] == 1 and i == (len(interactG)-1):
            end_timesG.append(format(i/66, ".8f"))
            end_timestampsG.append(str(datetime.timedelta(seconds=i//66)))
        elif interactG[i] == 1 and interactG[i + 1] == 0:
            end_timesG.append(format(i/66, ".8f"))
            end_timestampsG.append(str(datetime.timedelta(seconds=i//66)))
        # hole H interactions
        if interactH[i] == 1 and i == 0:
            start_timesH.append(format(i/66, ".8f"))
            start_timestampsH.append(str(datetime.timedelta(seconds=i//66)))
        elif interactH[i] == 1 and interactH[i - 1] == 0:
            start_timesH.append(format(i/66, ".8f"))
            start_timestampsH.append(str(datetime.timedelta(seconds=i//66)))
        if interactH[i] == 1 and i == (len(interactH)-1):
            end_timesH.append(format(i/66, ".8f"))
            end_timestampsH.append(str(datetime.timedelta(seconds=i//66)))
        elif interactH[i] == 1 and interactH[i + 1] == 0:
            end_timesH.append(format(i/66, ".8f"))
            end_timestampsH.append(str(datetime.timedelta(seconds=i//66)))
        # hole I interactions
        if interactI[i] == 1 and i == 0:
            start_timesI.append(format(i/66, ".8f"))
            start_timestampsI.append(str(datetime.timedelta(seconds=i//66)))
        elif interactI[i] == 1 and interactI[i - 1] == 0:
            start_timesI.append(format(i/66, ".8f"))
            start_timestampsI.append(str(datetime.timedelta(seconds=i//66)))
        if interactI[i] == 1 and i == (len(interactI)-1):
            end_timesI.append(format(i/66, ".8f"))
            end_timestampsI.append(str(datetime.timedelta(seconds=i//66)))
        elif interactI[i] == 1 and interactI[i + 1] == 0:
            end_timesI.append(format(i/66, ".8f"))
            end_timestampsI.append(str(datetime.timedelta(seconds=i//66)))
        # hole J interactions
        if interactJ[i] == 1 and i == 0:
            start_timesJ.append(format(i/66, ".8f"))
            start_timestampsJ.append(str(datetime.timedelta(seconds=i//66)))
        elif interactJ[i] == 1 and interactJ[i - 1] == 0:
            start_timesJ.append(format(i/66, ".8f"))
            start_timestampsJ.append(str(datetime.timedelta(seconds=i//66)))
        if interactJ[i] == 1 and i == (len(interactJ)-1):
            end_timesJ.append(format(i/66, ".8f"))
            end_timestampsJ.append(str(datetime.timedelta(seconds=i//66)))
        elif interactJ[i] == 1 and interactJ[i + 1] == 0:
            end_timesJ.append(format(i/66, ".8f"))
            end_timestampsJ.append(str(datetime.timedelta(seconds=i//66)))
        # hole K interactions
        if interactK[i] == 1 and i == 0:
            start_timesK.append(format(i/66, ".8f"))
            start_timestampsK.append(str(datetime.timedelta(seconds=i//66)))
        elif interactK[i] == 1 and interactK[i - 1] == 0:
            start_timesK.append(format(i/66, ".8f"))
            start_timestampsK.append(str(datetime.timedelta(seconds=i//66)))
        if interactK[i] == 1 and i == (len(interactK)-1):
            end_timesK.append(format(i/66, ".8f"))
            end_timestampsK.append(str(datetime.timedelta(seconds=i//66)))
        elif interactK[i] == 1 and interactK[i + 1] == 0:
            end_timesK.append(format(i/66, ".8f"))
            end_timestampsK.append(str(datetime.timedelta(seconds=i//66)))
        # hole L interactions
        if interactL[i] == 1 and i == 0:
            start_timesL.append(format(i/66, ".8f"))
            start_timestampsL.append(str(datetime.timedelta(seconds=i//66)))
        elif interactL[i] == 1 and interactL[i - 1] == 0:
            start_timesL.append(format(i/66, ".8f"))
            start_timestampsL.append(str(datetime.timedelta(seconds=i//66)))
        if interactL[i] == 1 and i == (len(interactL)-1):
            end_timesL.append(format(i/66, ".8f"))
            end_timestampsL.append(str(datetime.timedelta(seconds=i//66)))
        elif interactL[i] == 1 and interactL[i + 1] == 0:
            end_timesL.append(format(i/66, ".8f"))
            end_timestampsL.append(str(datetime.timedelta(seconds=i//66)))
        # hole M interactions
        if interactM[i] == 1 and i == 0:
            start_timesM.append(format(i/66, ".8f"))
            start_timestampsM.append(str(datetime.timedelta(seconds=i//66)))
        elif interactM[i] == 1 and interactM[i - 1] == 0:
            start_timesM.append(format(i/66, ".8f"))
            start_timestampsM.append(str(datetime.timedelta(seconds=i//66)))
        if interactM[i] == 1 and i == (len(interactM)-1):
            end_timesM.append(format(i/66, ".8f"))
            end_timestampsM.append(str(datetime.timedelta(seconds=i//66)))
        elif interactM[i] == 1 and interactM[i + 1] == 0:
            end_timesM.append(format(i/66, ".8f"))
            end_timestampsM.append(str(datetime.timedelta(seconds=i//66)))
        # hole N interactions
        if interactN[i] == 1 and i == 0:
            start_timesN.append(format(i/66, ".8f"))
            start_timestampsN.append(str(datetime.timedelta(seconds=i//66)))
        elif interactN[i] == 1 and interactN[i - 1] == 0:
            start_timesN.append(format(i/66, ".8f"))
            start_timestampsN.append(str(datetime.timedelta(seconds=i//66)))
        if interactN[i] == 1 and i == (len(interactN)-1):
            end_timesN.append(format(i/66, ".8f"))
            end_timestampsN.append(str(datetime.timedelta(seconds=i//66)))
        elif interactN[i] == 1 and interactN[i + 1] == 0:
            end_timesN.append(format(i/66, ".8f"))
            end_timestampsN.append(str(datetime.timedelta(seconds=i//66)))
        # hole O interactions
        if interactO[i] == 1 and i == 0:
            start_timesO.append(format(i/66, ".8f"))
            start_timestampsO.append(str(datetime.timedelta(seconds=i//66)))
        elif interactO[i] == 1 and interactO[i - 1] == 0:
            start_timesO.append(format(i/66, ".8f"))
            start_timestampsO.append(str(datetime.timedelta(seconds=i//66)))
        if interactO[i] == 1 and i == (len(interactO)-1):
            end_timesO.append(format(i/66, ".8f"))
            end_timestampsO.append(str(datetime.timedelta(seconds=i//66)))
        elif interactO[i] == 1 and interactO[i + 1] == 0:
            end_timesO.append(format(i/66, ".8f"))
            end_timestampsO.append(str(datetime.timedelta(seconds=i//66)))
        # hole P interactions
        if interactP[i] == 1 and i == 0:
            start_timesP.append(format(i/66, ".8f"))
            start_timestampsP.append(str(datetime.timedelta(seconds=i//66)))
        elif interactP[i] == 1 and interactP[i - 1] == 0:
            start_timesP.append(format(i/66, ".8f"))
            start_timestampsP.append(str(datetime.timedelta(seconds=i//66)))
        if interactP[i] == 1 and i == (len(interactP)-1):
            end_timesP.append(format(i/66, ".8f"))
            end_timestampsP.append(str(datetime.timedelta(seconds=i//66)))
        elif interactP[i] == 1 and interactP[i + 1] == 0:
            end_timesP.append(format(i/66, ".8f"))
            end_timestampsP.append(str(datetime.timedelta(seconds=i//66)))
        # hole Q interactions
        if interactQ[i] == 1 and i == 0:
            start_timesQ.append(format(i/66, ".8f"))
            start_timestampsQ.append(str(datetime.timedelta(seconds=i//66)))
        elif interactQ[i] == 1 and interactQ[i - 1] == 0:
            start_timesQ.append(format(i/66, ".8f"))
            start_timestampsQ.append(str(datetime.timedelta(seconds=i//66)))
        if interactQ[i] == 1 and i == (len(interactQ)-1):
            end_timesQ.append(format(i/66, ".8f"))
            end_timestampsQ.append(str(datetime.timedelta(seconds=i//66)))
        elif interactQ[i] == 1 and interactQ[i + 1] == 0:
            end_timesQ.append(format(i/66, ".8f"))
            end_timestampsQ.append(str(datetime.timedelta(seconds=i//66)))
        # hole R interactions
        if interactR[i] == 1 and i == 0:
            start_timesR.append(format(i/66, ".8f"))
            start_timestampsR.append(str(datetime.timedelta(seconds=i//66)))
        elif interactR[i] == 1 and interactR[i - 1] == 0:
            start_timesR.append(format(i/66, ".8f"))
            start_timestampsR.append(str(datetime.timedelta(seconds=i//66)))
        if interactR[i] == 1 and i == (len(interactR)-1):
            end_timesR.append(format(i/66, ".8f"))
            end_timestampsR.append(str(datetime.timedelta(seconds=i//66)))
        elif interactR[i] == 1 and interactR[i + 1] == 0:
            end_timesR.append(format(i/66, ".8f"))
            end_timestampsR.append(str(datetime.timedelta(seconds=i//66)))
        # hole S interactions
        if interactS[i] == 1 and i == 0:
            start_timesS.append(format(i/66, ".8f"))
            start_timestampsS.append(str(datetime.timedelta(seconds=i//66)))
        elif interactS[i] == 1 and interactS[i - 1] == 0:
            start_timesS.append(format(i/66, ".8f"))
            start_timestampsS.append(str(datetime.timedelta(seconds=i//66)))
        if interactS[i] == 1 and i == (len(interactS)-1):
            end_timesS.append(format(i/66, ".8f"))
            end_timestampsS.append(str(datetime.timedelta(seconds=i//66)))
        elif interactS[i] == 1 and interactS[i + 1] == 0:
            end_timesS.append(format(i/66, ".8f"))
            end_timestampsS.append(str(datetime.timedelta(seconds=i//66)))
        # hole T interactions
        if interactT[i] == 1 and i == 0:
            start_timesT.append(format(i/66, ".8f"))
            start_timestampsT.append(str(datetime.timedelta(seconds=i//66)))
        elif interactT[i] == 1 and interactT[i - 1] == 0:
            start_timesT.append(format(i/66, ".8f"))
            start_timestampsT.append(str(datetime.timedelta(seconds=i//66)))
        if interactT[i] == 1 and i == (len(interactT)-1):
            end_timesT.append(format(i/66, ".8f"))
            end_timestampsT.append(str(datetime.timedelta(seconds=i//66)))
        elif interactT[i] == 1 and interactT[i + 1] == 0:
            end_timesT.append(format(i/66, ".8f"))
            end_timestampsT.append(str(datetime.timedelta(seconds=i//66)))

    #add interaction times to a new file
    event_file = open(file_name + '_events.csv', 'w')
    csvwriter = csv.writer(event_file)
    csvwriter.writerow(["object","events","start times (s)","end times (s)","start timestamps (mm:ss)","end timestamps (mm:ss)"])
    for i in range(len(start_times_escape)):
        csvwriter.writerow(["escape",i+1,start_times_escape[i],end_times_escape[i],start_timestamps_escape[i],end_timestamps_escape[i]])
    for i in range(len(start_timesB)):
        csvwriter.writerow(["B",i+1,start_timesB[i],end_timesB[i],start_timestampsB[i],end_timestampsB[i]])
    for i in range(len(start_timesC)):
        csvwriter.writerow(["C",i+1,start_timesC[i],end_timesC[i],start_timestampsC[i],end_timestampsC[i]])
    for i in range(len(start_timesD)):
        csvwriter.writerow(["D",i+1,start_timesD[i],end_timesD[i],start_timestampsD[i],end_timestampsD[i]])
    for i in range(len(start_timesE)):
        csvwriter.writerow(["E",i+1,start_timesE[i],end_timesE[i],start_timestampsE[i],end_timestampsE[i]])
    for i in range(len(start_timesF)):
        csvwriter.writerow(["F",i+1,start_timesF[i],end_timesF[i],start_timestampsF[i],end_timestampsF[i]])
    for i in range(len(start_timesG)):
        csvwriter.writerow(["G",i+1,start_timesG[i],end_timesG[i],start_timestampsG[i],end_timestampsG[i]])
    for i in range(len(start_timesH)):
        csvwriter.writerow(["H",i+1,start_timesH[i],end_timesH[i],start_timestampsH[i],end_timestampsH[i]])
    for i in range(len(start_timesI)):
        csvwriter.writerow(["I",i+1,start_timesI[i],end_timesI[i],start_timestampsI[i],end_timestampsI[i]])
    for i in range(len(start_timesJ)):
        csvwriter.writerow(["J",i+1,start_timesJ[i],end_timesJ[i],start_timestampsJ[i],end_timestampsJ[i]])
    for i in range(len(start_timesK)):
        csvwriter.writerow(["K",i+1,start_timesK[i],end_timesK[i],start_timestampsK[i],end_timestampsK[i]])
    for i in range(len(start_timesL)):
        csvwriter.writerow(["L",i+1,start_timesL[i],end_timesL[i],start_timestampsL[i],end_timestampsL[i]])
    for i in range(len(start_timesM)):
        csvwriter.writerow(["M",i+1,start_timesM[i],end_timesM[i],start_timestampsM[i],end_timestampsM[i]])
    for i in range(len(start_timesN)):
        csvwriter.writerow(["N",i+1,start_timesN[i],end_timesN[i],start_timestampsN[i],end_timestampsN[i]])
    for i in range(len(start_timesO)):
        csvwriter.writerow(["O",i+1,start_timesO[i],end_timesO[i],start_timestampsO[i],end_timestampsO[i]])
    for i in range(len(start_timesP)):
        csvwriter.writerow(["P",i+1,start_timesP[i],end_timesP[i],start_timestampsP[i],end_timestampsP[i]])
    for i in range(len(start_timesQ)):
        csvwriter.writerow(["Q",i+1,start_timesQ[i],end_timesQ[i],start_timestampsQ[i],end_timestampsQ[i]])
    for i in range(len(start_timesR)):
        csvwriter.writerow(["R",i+1,start_timesR[i],end_timesR[i],start_timestampsR[i],end_timestampsR[i]])
    for i in range(len(start_timesS)):
        csvwriter.writerow(["S",i+1,start_timesS[i],end_timesS[i],start_timestampsS[i],end_timestampsS[i]])
    for i in range(len(start_timesT)):
        csvwriter.writerow(["T",i+1,start_timesT[i],end_timesT[i],start_timestampsT[i],end_timestampsT[i]])
    event_file.close()
    #report the length of time the mouse spends interacting with each object
    intervals_escape,intervals_B,intervals_C,intervals_D,intervals_E,intervals_F,intervals_G,intervals_H,intervals_I,intervals_J,intervals_K,intervals_L,intervals_M,intervals_N,intervals_O,intervals_P,intervals_Q,intervals_R,intervals_S,intervals_T = ([] for i in range(20))
    total_time_escape,total_time_B,total_time_C,total_time_D,total_time_E,total_time_F,total_time_G,total_time_H,total_time_I,total_time_J,total_time_K,total_time_L,total_time_M,total_time_N,total_time_O,total_time_P,total_time_Q,total_time_R,total_time_S,total_time_T = (0,)*20
    for i in range(0, len(start_times_escape)):
        time = float(end_times_escape[i])-float(start_times_escape[i])
        intervals_escape.append(format(time, ".8f"))
        total_time_escape += time
    for i in range(0, len(start_timesB)):
        time = float(end_timesB[i])-float(start_timesB[i])
        intervals_B.append(format(time, ".8f"))
        total_time_B += time
    for i in range(0, len(start_timesC)):
        time = float(end_timesC[i])-float(start_timesC[i])
        intervals_C.append(format(time, ".8f"))
        total_time_C += time
    for i in range(0, len(start_timesD)):
        time = float(end_timesD[i])-float(start_timesD[i])
        intervals_D.append(format(time, ".8f"))
        total_time_D += time
    for i in range(0, len(start_timesE)):
        time = float(end_timesE[i])-float(start_timesE[i])
        intervals_E.append(format(time, ".8f"))
        total_time_E += time
    for i in range(0, len(start_timesF)):
        time = float(end_timesF[i])-float(start_timesF[i])
        intervals_F.append(format(time, ".8f"))
        total_time_F += time
    for i in range(0, len(start_timesG)):
        time = float(end_timesG[i])-float(start_timesG[i])
        intervals_G.append(format(time, ".8f"))
        total_time_G += time
    for i in range(0, len(start_timesH)):
        time = float(end_timesH[i])-float(start_timesH[i])
        intervals_H.append(format(time, ".8f"))
        total_time_H += time
    for i in range(0, len(start_timesI)):
        time = float(end_timesI[i])-float(start_timesI[i])
        intervals_I.append(format(time, ".8f"))
        total_time_I += time
    for i in range(0, len(start_timesJ)):
        time = float(end_timesJ[i])-float(start_timesJ[i])
        intervals_J.append(format(time, ".8f"))
        total_time_J += time
    for i in range(0, len(start_timesK)):
        time = float(end_timesK[i])-float(start_timesK[i])
        intervals_K.append(format(time, ".8f"))
        total_time_K += time
    for i in range(0, len(start_timesL)):
        time = float(end_timesL[i])-float(start_timesL[i])
        intervals_L.append(format(time, ".8f"))
        total_time_L += time
    for i in range(0, len(start_timesM)):
        time = float(end_timesM[i])-float(start_timesM[i])
        intervals_M.append(format(time, ".8f"))
        total_time_M += time
    for i in range(0, len(start_timesN)):
        time = float(end_timesN[i])-float(start_timesN[i])
        intervals_N.append(format(time, ".8f"))
        total_time_N += time
    for i in range(0, len(start_timesO)):
        time = float(end_timesO[i])-float(start_timesO[i])
        intervals_O.append(format(time, ".8f"))
        total_time_O += time
    for i in range(0, len(start_timesP)):
        time = float(end_timesP[i])-float(start_timesP[i])
        intervals_P.append(format(time, ".8f"))
        total_time_P += time
    for i in range(0, len(start_timesQ)):
        time = float(end_timesQ[i])-float(start_timesQ[i])
        intervals_Q.append(format(time, ".8f"))
        total_time_Q += time
    for i in range(0, len(start_timesR)):
        time = float(end_timesR[i])-float(start_timesR[i])
        intervals_R.append(format(time, ".8f"))
        total_time_R += time
    for i in range(0, len(start_timesS)):
        time = float(end_timesS[i])-float(start_timesS[i])
        intervals_S.append(format(time, ".8f"))
        total_time_S += time
    for i in range(0, len(start_timesT)):
        time = float(end_timesT[i])-float(start_timesT[i])
        intervals_T.append(format(time, ".8f"))
        total_time_T += time
    print(f"Interaction Intervals (escape): {intervals_escape}")
    print(f"Total Time (escape): {format(total_time_escape, '.8f')} s")
    print(f"Total Time (B): {format(total_time_B, '.8f')} s")
    print(f"Total Time (C): {format(total_time_C, '.8f')} s")
    print(f"Total Time (D): {format(total_time_D, '.8f')} s")
    print(f"Total Time (E): {format(total_time_E, '.8f')} s")
    print(f"Total Time (F): {format(total_time_F, '.8f')} s")
    print(f"Total Time (G): {format(total_time_G, '.8f')} s")
    print(f"Total Time (H): {format(total_time_H, '.8f')} s")
    print(f"Total Time (I): {format(total_time_I, '.8f')} s")
    print(f"Total Time (J): {format(total_time_J, '.8f')} s")
    print(f"Total Time (K): {format(total_time_K, '.8f')} s")
    print(f"Total Time (L): {format(total_time_L, '.8f')} s")
    print(f"Total Time (M): {format(total_time_M, '.8f')} s")
    print(f"Total Time (N): {format(total_time_N, '.8f')} s")
    print(f"Total Time (O): {format(total_time_O, '.8f')} s")
    print(f"Total Time (P): {format(total_time_P, '.8f')} s")
    print(f"Total Time (Q): {format(total_time_Q, '.8f')} s")
    print(f"Total Time (R): {format(total_time_R, '.8f')} s")
    print(f"Total Time (S): {format(total_time_S, '.8f')} s")
    print(f"Total Time (T): {format(total_time_T, '.8f')} s")
