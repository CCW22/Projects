import os
import datetime
import pandas as pd
import xlrd
import numpy as np

def summaryfile(path_to_excel_file):
    vel_p1_list = []
    vel_p2_list = []
    vel_p3_list = []
    vel_pavg_list = []
    vel_ds1_list = []
    vel_dan_list = []
    vel_ds7_list = []
    vel_f_list = []
    pref_vels = []
    pref_avg_list = []
    subject_list = []
    dtc_list = []
    excel_df = pd.read_excel(path_to_excel_file)
    valid_subjects = excel_df["SUBJECT"]     #list of all the subject names in excel file
    for file in os.listdir(r"O:\Data\OND01\Analyzed_data\Stopwatch_speed"):
        if file.endswith(".txt"):
            file_name_split = os.path.basename(file).split("_")
            if file_name_split[3] == "02":        #finds V1 of each participant
                subject = "_".join(file_name_split[:3])
                print(subject)
                valid_subjects_list = valid_subjects.tolist()
                if subject in valid_subjects_list:
                    x = open(os.path.join(r"O:\Data\OND01\Analyzed_data\Stopwatch_speed", file), 'r')
                    pref_vels = []
                    #print("yaya", x)
                    read_lines = x.readlines()
                    fast_count = 0
                    serial1s_count = 0
                    serial7s_count = 0
                    animal_count = 0
                    dtc_count = 0
                    for line in read_lines:
                        split_lines = line.split(",")
                        if split_lines[-1][-2] == "*":
                            dec_index = split_lines[-1].index("(m/s)")
                            pref_vels.append(float(split_lines[-1][:dec_index]))
                            pref_avg = np.mean(pref_vels)
                        if "serial1s" in split_lines[0]:
                            serial1s_count += 1
                            ds1_index = split_lines[3].index("(m/s)")
                            vel_ds1_temp = split_lines[3][:ds1_index]
                        if "serial7s" in split_lines[0]:
                            serial7s_count += 1
                            ds7_index = split_lines[3].index("(m/s)")
                            vel_ds7_temp = split_lines[3][:ds7_index]
                        if "animal" in split_lines[0]:
                            animal_count += 1
                            dan_index = split_lines[3].index("(m/s)")
                            vel_dan_temp = split_lines[3][:dan_index]
                        if "fast" in split_lines[0]:
                            fast_count += 1
                            f_index = split_lines[3].index("(m/s)")
                            vel_f_temp = split_lines[3][:f_index]
                        if "(%)" in split_lines:
                            dtc = split_lines[:split_lines.index("(%)")]
                    dtc_list.append(dtc)
                    if serial1s_count == 1:
                        vel_ds1_list.append(vel_ds1_temp)
                    else:
                        vel_ds1_list.append(None)
                        print("VEL DS1 WRONG COUNT FOR FILE", file)
                    if serial7s_count == 1:
                        vel_ds7_list.append(vel_ds7_temp)
                    else:
                        vel_ds7_list.append(None)
                        print("VEL DS7 WRONG COUNT FOR FILE", file)
                    if animal_count == 1:
                        vel_dan_list.append(vel_dan_temp)
                    else:
                        vel_dan_list.append(None)
                        print("VEL DAN WRONG COUNT FOR FILE", file)
                    if fast_count == 1:
                        vel_f_list.append(vel_f_temp)
                    else:
                        vel_f_list.append(None)
                        print("VEL FAST WRONG COUNT FOR FILE", file)
                    #if dtc_count == 1:
                        #dtc_list.append(dtc_temp)
                    #else:
                        #dtc_list.append(None)
                        #print("DTC WRONG COUNT FOR FILE", file)
                    try:
                        vel_p1_list.append(pref_vels[0])
                    except(IndexError):
                        vel_p1_list.append(None)
                        print("NONE INPUTTED FOR vel_p1_list FOR FILE", file)
                    try:
                        vel_p2_list.append(pref_vels[1])
                    except(IndexError):
                        vel_p2_list.append(None)
                        print("NONE INPUTTED FOR vel_p2_list FOR FILE", file)
                    try:
                        vel_p3_list.append(pref_vels[2])
                    except(IndexError):
                        vel_p3_list.append(None)
                        print("NONE INPUTTED FOR vel_p3_list FOR FILE", file)

                    pref_avg_list.append(pref_avg)
                    subject_list.append(subject)
                else:
                    print(False)

    print("fast", len(vel_f_list))
    print("d7", len(vel_ds7_list))
    print("animal", len(vel_dan_list))
    print("d1", len(vel_ds1_list))
    print("3", len(vel_p3_list))
    print("2", len(vel_p2_list))
    print("1", len(vel_p1_list))
    print("avg", len(pref_avg_list))
    print("val", len(subject_list))
    print("dtc", len(dtc_list))

    df_dict = {"SUBJECT": subject_list,
               "STOP_P1_SS_VELOCITY": vel_p1_list,
               "STOP_P2_SS_VELOCITY": vel_p2_list,
               "STOP_P3_SS_VELOCITY": vel_p3_list,
               "STOP_Pavg_SS_VELOCITY": pref_avg_list,
               "STOP_DS1_SS_VELOCITY": vel_ds1_list,
               "STOP_DAn_SS_VELOCITY": vel_dan_list,
               "STOP_DS7_SS_VELOCITY": vel_ds7_list,
               "STOP_F_SS_VELOCITY": vel_f_list,
               "STOP_DS1_SS_DTC": dtc_list}

    summary_list_df = pd.DataFrame(df_dict)
    print(summary_list_df)
    summary_list_df.to_excel(r"C:\Users\chris\OneDrive\Documents\Year 2 Term 2\Stopwatch_speed_gait methods.xlsx",index=False)
    return summary_list_df
x = summaryfile(r'C:\Users\chris\Downloads\Stopwatch speeds_gait methods.xlsx')
