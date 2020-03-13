import itertools
import numpy as np
import os
import datetime
from combinations_std import *

def velocity_maker(path_to_text_file):
    x = open(path_to_text_file, 'r')
    data = x.readlines()
    last_modified_s = os.path.getmtime(path_to_text_file)
    last_modified = datetime.datetime.fromtimestamp(last_modified_s)
    print("last modified", last_modified)
    distance_dict = {"normal":6,
                     "TOH":7.62,
                     "EBH":6.59892,
                     "CAM":7.62,
                     "BYC":6.5344}
    last_modified_test = "normal"
    if datetime.datetime(year = 2016, month = 4, day = 26) >= last_modified:
        if "_TOH_" in path_to_text_file:
            last_modified_test = "TOH"
    if datetime.datetime(year=2016, month=4, day=19) >= last_modified:
        if "_EBH_" in path_to_text_file:
            last_modified_test = "EBH"
        if "_CAM_" in path_to_text_file:
            last_modified_test = "CAM"
    if datetime.datetime(year=2016, month=4, day=14) <= last_modified:
        if "_BYC_" in path_to_text_file:
            last_modified_test = "BYC"

    #newtest = [x[:-5] for x in test]
    print("Starting velocity maker on", path_to_text_file, "...")
    walktype = []
    walktime = []
    pref_walktime = []
    dual_walktime =[]
    velocity = []
    dt_velocity = []
    time_stamp = []
    pref_velocity = []
    dual_bool = []
    newdata = [x[:-1] for x in data]
    for element in range(len(data)):
        type = data[element].split(",")
        #print(type)
        #dual_bool is used to determine if the line in the acc_index is a dual task walk
        if ("serial1s" in type) or ("animal" in type) or ("serial7s" in type):
            dual_bool.append(True)
        else:
            dual_bool.append(False)
        #print(dual_bool)

        #assignment of variables for preferred and fast walks, and determining the velocity of each preferred walk (line contains 3 elements: pref, timestamp, time)
        if len(type) == 3:
            walk = type[0]
            time_list = [s for s in type if "(s)" in s]  # always will only have 1 value (i hope)
            time = time_list[0]
            if len(time) > 12:
                time_s = float(time[0:8])
            else:
                time_s = float(time[:-4])
            if time_s == 0:
                print("TIME IS 0 SECONDS, VELOCITY UNDEFINED")
                vel = "undefined"
            else:
                vel = round(distance_dict[last_modified_test] /time_s,3)
            walktype.append(walk)
            walktime.append(time_s)
            velocity.append(vel)
            if walk == "pref" and ( type[1].endswith(("PM", "AM")) )and ( time_s != 0 ):
                pref_walktime.append(time_s)
            for n in range(len(type)):
                if type[n].endswith(("PM", "AM")):
                    time_stamp.append(type[n])

        #assignment of variables for preferred and fast walks, and determining the velocity of each preferred and fast walk (line contains 4 elements)
        elif len(type) >=4:
            if (type[0] == "pref") or (type[0] == "fast"):
                walk = type[0]
                walk_dual = type[1]
                time_list = [s for s in type if "(s)" in s]  # always will only have 1 value (i hope)
                time = time_list[0]
                time_s = float(time[:-4])
                if time_s == 0:
                    print("TIME IS 0 SECONDS, VELOCITY UNDEFINED")
                    vel = "undefined"
                else:
                    vel = round(distance_dict[last_modified_test] /time_s,3)
                walktype.append(walk + " " + walk_dual)
                walktime.append(time_s)
                velocity.append(vel)
                if walk == "pref" and ( type[1].endswith(("PM", "AM")) )and ( time_s != 0):
                    pref_walktime.append(time_s)
                for n in range(len(type)):
                    if type[n].endswith(("PM", "AM")):
                        time_stamp.append(type[n])
            else:
                walk = type[1]
                walk_dual = type[2]
                time_list = [s for s in type if "(s)" in s] # always will only have 1 value (i hope)
                time = time_list[0]
                time_s = float(time[:-4])
                #print(time_s)
                if time_s == 0:
                    print("TIME IS 0 SECONDS, VELOCITY UNDEFINED")
                    vel = "undefined"
                else:
                    vel = round(distance_dict[last_modified_test] /time_s,3)
                walktype.append(walk + " " + walk_dual)
                walktime.append(time_s)
                velocity.append(vel)
                if walk == "pref" and ( type[2].endswith(("PM", "AM")) ) and ( time_s != 0 ):
                    pref_walktime.append(time_s)
                for n in range(len(type)):
                    if type[n].endswith(("PM", "AM")):
                        time_stamp.append(type[n])

            #determining the dual task walking velocities
            if "serial1s" or "animal" or "serial7s" in type:
                dual_walktime.append(time_s)
                #print(time_s)
                #print(dual_walktime)
                if time_s == 0:
                    print("TIME IS 0 SECONDS, VELOCITY UNDEFINED")
                    dt_vel = "undefined"
                else:
                    dt_vel = round(distance_dict[last_modified_test] /time_s,3)
                    dt_velocity.append(dt_vel)
                #print("dt_velocities" , dt_velocity)

            #print(dual_walktime)
    #print(pref_walktime)

    #determining the lowest standard deviation combination of the preferred walks to rule out unreasonable times
    if len(pref_walktime) >= 3:
        preferred_walks = lowest_std_comb(pref_walktime, 3)
    elif len(pref_walktime) == 2:
        preferred_walks = lowest_std_comb(pref_walktime, 2)
    elif len(pref_walktime) == 1:
        preferred_walks = lowest_std_comb(pref_walktime, 1) # output is the time_s values of the good lines in the format (t1, t2, t3)
    else:
        print("NO PREF WALKS")
        preferred_walks = None
    #print(preferred_walks)
    pref_vels = []
    wanted_pref_lines = []
    #print("preferred_walks: ", preferred_walks)
    if preferred_walks != None:
        for n in preferred_walks:
            wanted_pref_lines.append(walktime.index(n))
            pref_vels.append(velocity[walktime.index(n)])

    #print("Good Lines: ",wanted_pref_lines)
    #print("pref vels: ", pref_vels)
    #print("pref vels average", np.average(pref_vels))

    #determining the dual task cost of each dual task by using the equation
    dual_task_cost = []
    dtc = abs((((dt_velocity) - np.average(pref_vels)) / (np.average(pref_vels))) * 100)
    rounded_dtc = np.round(dtc,3)
    dual_task_cost.append(rounded_dtc)
    dual_task_cost = dual_task_cost[0]
    #print("dtc" , dual_task_cost)

    #dt_vel = []
    #dual_task_cost = []
    #dt_vel.append(velocity[3:6])
    #dtc = (((dt_vel ) - np.average(pref_vels)) / (np.average(pref_vels))) * 100
    #print(dtc)
    #dual_task_cost.append(dtc)
    #print("Dual Task Cost(%):", dual_task_cost)

    #indicating the reasonable preferred walk lines in the acc_index
    wanted_lines_bool = [False]*len(data)
    for n in wanted_pref_lines:
        #print(n)
        wanted_lines_bool[n] = True
    #print(wanted_lines_bool)

    #print(dual_bool)
    #print(dual_task_cost)

    #outputting the data into a file, includes the velocity and dual task cost
    #the * indicates the reasonable/wanted preferred walk lines in the file
    output_data = []
    dual_num = 0
    for n in range(len(walktype)):
        if ( dual_bool[n] == True ) and ( walktime[n] != 0):
            #print(str(dual_task_cost[dual_num]))
            output_data.append(str(walktype[n])+", " + str(time_stamp[n]) + ", " + str(walktime[n]) +"(s)" + ", " + str(velocity[n]) + "(m/s)" + "," + str(dual_task_cost[dual_num]) + "(%)")
            dual_num += 1
        elif wanted_lines_bool[n] == True:
            output_data.append(str(walktype[n])+", " + str(time_stamp[n]) + ", " + str(walktime[n]) +"(s)" + ", " + str(velocity[n]) + "(m/s)" + " " + "*")

        else:
            output_data.append(str(walktype[n]) + ", " + str(time_stamp[n]) + ", " + str(walktime[n]) + "(s)" + ", " + str(velocity[n]) + "(m/s)")
    print("output data: ", output_data)

    new_filepath = os.path.join(r'O:\Data\OND01\Analyzed_data\Stopwatch_speed',os.path.basename(path_to_text_file)[:-13] + "stopwatch.txt")


    #with open(new_filepath,"w") as output_file: #path_to_text_file[:-3] +
        #for x in output_data:
            #output_file.write("%s\n" % x)

    print("New file outputted to:", new_filepath)
    print("Finished velocity conversion of:", path_to_text_file)

    #newwalktime: List[str] = [x[:-1] for x in walktime]

    #print(walktype)
    #print(walktime)
    #print(velocity)
    #print(time_stamp)
    # output_data.append("The average of the velocites: " + str(sum(velocity)/len(velocity)))








