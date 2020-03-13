import itertools
import os
import datetime
import pandas as pd

def summaryfile(path_to_dir):
    walk_task_list = []
    date_list = []
    stopwatch_time_list = []
    velocity_list = []
    dtc_list = []
    site_list = []
    subject_list =[]
    visit_list = []
    valid_pref_walk_list = []
    for file_name in os.listdir(path_to_dir):
        x = open(os.path.join(path_to_dir, file_name), 'r')
        data = x.readlines()
        split_file = file_name.split("_")
        site = split_file[1]
        subject = split_file[2]
        visit = split_file[3]
        for line in data:
                #print(os.path.basename(file_name).split("_")[2])
            if line[-2] == "*":
                valid_pref_walk = True
            else:
                valid_pref_walk = False
            type = line.split(",")
            stopwatch_time = None
            velocity = None
            dtc = None
            date = None
            walk_task = None
            for split_value in type:
                if "pref" in split_value:
                    walk_task = split_value[:split_value.index("f")+1]
                if "fast" in split_value:
                    walk_task = split_value[:split_value.index("t")+1]
                if "serial" in split_value:
                    walk_task = split_value[:split_value.index("s")+8]
                if "animal" in split_value:
                    walk_task = split_value[:split_value.index("l")+1]
                if split_value.endswith("(s)"):
                    stopwatch_time = split_value[:split_value.index("(s)")]
                if "(m/s)" in split_value:
                    velocity = split_value[:split_value.index("(m/s)")]
                if "(%)" in split_value:
                    dtc = split_value[:split_value.index("(%)")]
                if split_value.endswith("AM") or split_value.endswith("PM"):
                    date = split_value
            stopwatch_time_list.append(stopwatch_time)
            velocity_list.append(velocity)
            dtc_list.append(dtc)
            date_list.append(date)
            walk_task_list.append(walk_task)
            site_list.append(site)
            subject_list.append(subject)
            visit_list.append(visit)
            valid_pref_walk_list.append(valid_pref_walk)
    df_dict = {"Site": site_list,
               "Subject ID": subject_list,
               "Visit": visit_list,
               "Collection Time": date_list,
               "Walk Task": walk_task_list,
               "Stopwatch Time (s)": stopwatch_time_list,
               "Velocity (m/s)": velocity_list,
               "Dual Task Cost (%)": dtc_list,
               "Valid Pref Walk": valid_pref_walk_list}
    summary_list_df = pd.DataFrame(df_dict)
    print(summary_list_df)
    summary_list_df.to_excel(r"O:\Data\OND01\Analyzed_data\Stopwatch_speed\Stopwatch_time_Summary.xlsx",index=False)



summaryfile(r'O:\Data\OND01\Analyzed_data\Stopwatch_speed')

    #split_files = os.path.basename(path_to_text_file).split("_")
    #print(split_files)



