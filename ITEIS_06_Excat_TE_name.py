import pandas as pd
import pysam
import re
import os
def yq_Excat_Single_Str_at_list(old_all_site):
    new_all_site = []
    for temp in old_all_site:
        if temp not in new_all_site:
            new_all_site.append(temp)
    return new_all_site

f1 = open("All_File_Name", 'r')
line1 = f1.readline()
k2 = 0
yq_Time_set = []
while line1:
    if line1[-1] == '\n':
        TempLine1 = line1[0:-1]
    else:
        TempLine1 = line1
    Group = TempLine1
    print("Group = ",Group)


    Goal_Read_Name_and_Goal_Site_TJ = pd.read_csv("./" + Group + "/" + Group + "_Goal_Blat_res_eff_Map_TE.csv",sep=',',header=0,index_col=None)
    # print("Goal_Read_Name_and_Goal_Site_TJ = ",Goal_Read_Name_and_Goal_Site_TJ)
    temp_all_site = list(Goal_Read_Name_and_Goal_Site_TJ["Q_Site"])
    all_site = yq_Excat_Single_Str_at_list(temp_all_site)

    TE_Site_Name_TJ = pd.DataFrame(columns=["pd","pd_domain"])
    # print("all_site = ",all_site)
    # print("len(all_site) = ",len(all_site))
    k = 0
    #######################################################################################################################################
    for temp_site in all_site:
        goal_pd = Goal_Read_Name_and_Goal_Site_TJ[Goal_Read_Name_and_Goal_Site_TJ["Q_Site"]==temp_site]
        # print("goal_pd = ",goal_pd)

        goal_pd_Left_Right_BZ = goal_pd[((goal_pd["Q_end"] == 150) & (goal_pd["T_start"] == 0)) | (goal_pd["Q_start"] == 0) & (goal_pd["T_end"] == goal_pd["T_size"])]
        goal_pd_Left_BZ = goal_pd[(goal_pd["Q_end"] == 150) & (goal_pd["T_start"] == 0)]
        goal_pd_Right_BZ = goal_pd[(goal_pd["Q_start"] == 0) & (goal_pd["T_end"] == goal_pd["T_size"])]

        temp_goal_pd_Left_Right_BZ_name = goal_pd_Left_Right_BZ["T_name"]
        temp_goal_pd_Left_BZ_name = goal_pd_Left_BZ["T_name"]
        temp_goal_pd_Right_BZ_name = goal_pd_Right_BZ["T_name"]

        goal_pd_Left_Right_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_Right_BZ_name)
        goal_pd_Left_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_BZ_name)
        goal_pd_Right_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Right_BZ_name)

        k1 = 0
        for temp_name in goal_pd_Left_Right_BZ_name:
            if (temp_name in goal_pd_Left_BZ_name) & (temp_name in goal_pd_Right_BZ_name):
                TE_Site_Name_TJ.loc[temp_site,k1] = temp_name
                k1 = k1 + 1
        if k1 > 0:
            TE_Site_Name_TJ.loc[temp_site, "pd"] = "BZ"


    #######################################################################################################################################
    for temp_site in all_site:
        goal_pd_1 = TE_Site_Name_TJ[TE_Site_Name_TJ["pd"] == "BZ"]
        if temp_site not in list(goal_pd_1.index):

            goal_pd = Goal_Read_Name_and_Goal_Site_TJ[Goal_Read_Name_and_Goal_Site_TJ["Q_Site"]==temp_site]
            # print("goal_pd = ",goal_pd)

            goal_pd_Left_Right_BZ = goal_pd[((goal_pd["Q_end"] == 150) & (goal_pd["T_start"] == 0)) | (goal_pd["Q_start"] == 0) & (goal_pd["T_end"] == goal_pd["T_size"])]
            goal_pd_Left_BZ = goal_pd[(goal_pd["Q_end"] == 150) & (goal_pd["T_start"] == 0)]
            goal_pd_Right_BZ = goal_pd[(goal_pd["Q_start"] == 0) & (goal_pd["T_end"] == goal_pd["T_size"])]

            temp_goal_pd_Left_Right_BZ_name = goal_pd_Left_Right_BZ["T_name"]
            temp_goal_pd_Left_BZ_name = goal_pd_Left_BZ["T_name"]
            temp_goal_pd_Right_BZ_name = goal_pd_Right_BZ["T_name"]

            goal_pd_Left_Right_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_Right_BZ_name)
            goal_pd_Left_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_BZ_name)
            goal_pd_Right_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Right_BZ_name)

            k1 = 0
            for temp_name in goal_pd_Left_Right_BZ_name:
                if (temp_name in goal_pd_Left_BZ_name) & (temp_name not in goal_pd_Right_BZ_name):
                    TE_Site_Name_TJ.loc[temp_site, "Left_" + str(k1)] = temp_name
                    k1 = k1 + 1
            if k1 > 0:
                TE_Site_Name_TJ.loc[temp_site, "pd_domain"] = "BZ_Left"

    #######################################################################################################################################
    for temp_site in all_site:
        goal_pd_1 = TE_Site_Name_TJ[TE_Site_Name_TJ["pd"] == "BZ"]
        if temp_site not in list(goal_pd_1.index):
            goal_pd = Goal_Read_Name_and_Goal_Site_TJ[Goal_Read_Name_and_Goal_Site_TJ["Q_Site"]==temp_site]
            # print("goal_pd = ",goal_pd)

            goal_pd_Left_Right_BZ = goal_pd[((goal_pd["Q_end"] == 150) & (goal_pd["T_start"] == 0)) | (goal_pd["Q_start"] == 0) & (goal_pd["T_end"] == goal_pd["T_size"])]
            goal_pd_Left_BZ = goal_pd[(goal_pd["Q_end"] == 150) & (goal_pd["T_start"] == 0)]
            goal_pd_Right_BZ = goal_pd[(goal_pd["Q_start"] == 0) & (goal_pd["T_end"] == goal_pd["T_size"])]

            temp_goal_pd_Left_Right_BZ_name = goal_pd_Left_Right_BZ["T_name"]
            temp_goal_pd_Left_BZ_name = goal_pd_Left_BZ["T_name"]
            temp_goal_pd_Right_BZ_name = goal_pd_Right_BZ["T_name"]

            goal_pd_Left_Right_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_Right_BZ_name)
            goal_pd_Left_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_BZ_name)
            goal_pd_Right_BZ_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Right_BZ_name)

            k1 = 0
            for temp_name in goal_pd_Left_Right_BZ_name:
                if (temp_name not in goal_pd_Left_BZ_name) & (temp_name in goal_pd_Right_BZ_name):
                    TE_Site_Name_TJ.loc[temp_site, "Right_" + str(k1)] = temp_name
                    k1 = k1 + 1
            if k1 > 0:
                TE_Site_Name_TJ.loc[temp_site, "pd_domain"] = "BZ_Right"


    #######################################################################################################################################
    # print("TE_Site_Name_TJ = ",TE_Site_Name_TJ)
    for temp_site in all_site:
        goal_pd_1 = TE_Site_Name_TJ[TE_Site_Name_TJ["pd"] == "BZ"]
        if temp_site not in list(goal_pd_1.index):
            #print("temp_site = ",temp_site)
            goal_pd = Goal_Read_Name_and_Goal_Site_TJ[Goal_Read_Name_and_Goal_Site_TJ["Q_Site"] == temp_site]
            # print("goal_pd = ",goal_pd)


            goal_pd_Left_Right_BZFK = goal_pd[((goal_pd["Q_end"] >= 140) & (goal_pd["T_start"] <= 10)) | (
                        (goal_pd["Q_start"] <= 10) & (goal_pd["T_end"] >= goal_pd["T_size"] - 10))]
            goal_pd_Left_BZFK = goal_pd[(goal_pd["Q_end"] >= 140) & (goal_pd["T_start"] <= 10)]
            goal_pd_Right_BZFK = goal_pd[(goal_pd["Q_start"] <= 10) & (goal_pd["T_end"] >= goal_pd["T_size"] - 10)]

            temp_goal_pd_Left_Right_BZFK_name = goal_pd_Left_Right_BZFK["T_name"]
            temp_goal_pd_Left_BZFK_name = goal_pd_Left_BZFK["T_name"]
            temp_goal_pd_Right_BZFK_name = goal_pd_Right_BZFK["T_name"]

            goal_pd_Left_Right_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_Right_BZFK_name)
            goal_pd_Left_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_BZFK_name)
            goal_pd_Right_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Right_BZFK_name)
            #print("goal_pd_Left_Right_BZFK_name = ",goal_pd_Left_Right_BZFK_name)
            #print("goal_pd_Right_BZFK_name = ",goal_pd_Right_BZFK_name)
            #print("goal_pd_Left_BZFK_name = ",goal_pd_Left_BZFK_name)
            k1 = 0
            for temp_name in goal_pd_Left_Right_BZFK_name:
                if (temp_name in goal_pd_Left_BZFK_name) & (temp_name in goal_pd_Right_BZFK_name):
                    TE_Site_Name_TJ.loc[temp_site, k1] = temp_name
                    k1 = k1 + 1
            if k1 > 0:
                TE_Site_Name_TJ.loc[temp_site, "pd"] = "BZFK"


    #######################################################################################################################################
    # print("TE_Site_Name_TJ = ",TE_Site_Name_TJ)
    for temp_site in all_site:
        goal_pd_1 = TE_Site_Name_TJ[(TE_Site_Name_TJ["pd"] == "BZ")|(TE_Site_Name_TJ["pd"] == "BZFK")|(TE_Site_Name_TJ["pd_domain"] == "BZ_Right")|(TE_Site_Name_TJ["pd_domain"] == "BZ_Left")]
        if temp_site not in list(goal_pd_1.index):
            #print("temp_site = ",temp_site)
            goal_pd = Goal_Read_Name_and_Goal_Site_TJ[Goal_Read_Name_and_Goal_Site_TJ["Q_Site"] == temp_site]
            # print("goal_pd = ",goal_pd)


            goal_pd_Left_Right_BZFK = goal_pd[((goal_pd["Q_end"] >= 140) & (goal_pd["T_start"] <= 10)) | (
                        (goal_pd["Q_start"] <= 10) & (goal_pd["T_end"] >= goal_pd["T_size"] - 10))]
            goal_pd_Left_BZFK = goal_pd[(goal_pd["Q_end"] >= 140) & (goal_pd["T_start"] <= 10)]
            goal_pd_Right_BZFK = goal_pd[(goal_pd["Q_start"] <= 10) & (goal_pd["T_end"] >= goal_pd["T_size"] - 10)]

            temp_goal_pd_Left_Right_BZFK_name = goal_pd_Left_Right_BZFK["T_name"]
            temp_goal_pd_Left_BZFK_name = goal_pd_Left_BZFK["T_name"]
            temp_goal_pd_Right_BZFK_name = goal_pd_Right_BZFK["T_name"]

            goal_pd_Left_Right_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_Right_BZFK_name)
            goal_pd_Left_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_BZFK_name)
            goal_pd_Right_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Right_BZFK_name)
            #print("goal_pd_Left_Right_BZFK_name = ",goal_pd_Left_Right_BZFK_name)
            #print("goal_pd_Right_BZFK_name = ",goal_pd_Right_BZFK_name)
            #print("goal_pd_Left_BZFK_name = ",goal_pd_Left_BZFK_name)
            k1 = 0
            for temp_name in goal_pd_Left_Right_BZFK_name:
                if (temp_name in goal_pd_Left_BZFK_name) & (temp_name not in goal_pd_Right_BZFK_name):
                    TE_Site_Name_TJ.loc[temp_site, "Left_" + str(k1)] = temp_name
                    k1 = k1 + 1
            if k1 > 0:
                TE_Site_Name_TJ.loc[temp_site, "pd_domain"] = "BZFK_Left"


    #######################################################################################################################################
    # print("TE_Site_Name_TJ = ",TE_Site_Name_TJ)
    for temp_site in all_site:
        goal_pd_1 = TE_Site_Name_TJ[(TE_Site_Name_TJ["pd"] == "BZ")|(TE_Site_Name_TJ["pd"] == "BZFK")|(TE_Site_Name_TJ["pd_domain"] == "BZ_Right")|(TE_Site_Name_TJ["pd_domain"] == "BZ_Left")]
        if temp_site not in list(goal_pd_1.index):
            #print("temp_site = ",temp_site)
            goal_pd = Goal_Read_Name_and_Goal_Site_TJ[Goal_Read_Name_and_Goal_Site_TJ["Q_Site"] == temp_site]
            # print("goal_pd = ",goal_pd)


            goal_pd_Left_Right_BZFK = goal_pd[((goal_pd["Q_end"] >= 140) & (goal_pd["T_start"] <= 10)) | (
                        (goal_pd["Q_start"] <= 10) & (goal_pd["T_end"] >= goal_pd["T_size"] - 10))]
            goal_pd_Left_BZFK = goal_pd[(goal_pd["Q_end"] >= 140) & (goal_pd["T_start"] <= 10)]
            goal_pd_Right_BZFK = goal_pd[(goal_pd["Q_start"] <= 10) & (goal_pd["T_end"] >= goal_pd["T_size"] - 10)]

            temp_goal_pd_Left_Right_BZFK_name = goal_pd_Left_Right_BZFK["T_name"]
            temp_goal_pd_Left_BZFK_name = goal_pd_Left_BZFK["T_name"]
            temp_goal_pd_Right_BZFK_name = goal_pd_Right_BZFK["T_name"]

            goal_pd_Left_Right_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_Right_BZFK_name)
            goal_pd_Left_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Left_BZFK_name)
            goal_pd_Right_BZFK_name = yq_Excat_Single_Str_at_list(temp_goal_pd_Right_BZFK_name)
            #print("goal_pd_Left_Right_BZFK_name = ",goal_pd_Left_Right_BZFK_name)
            #print("goal_pd_Right_BZFK_name = ",goal_pd_Right_BZFK_name)
            #print("goal_pd_Left_BZFK_name = ",goal_pd_Left_BZFK_name)
            k1 = 0
            for temp_name in goal_pd_Left_Right_BZFK_name:
                if (temp_name not in goal_pd_Left_BZFK_name) & (temp_name in goal_pd_Right_BZFK_name):
                    TE_Site_Name_TJ.loc[temp_site, "Right_" + str(k1)] = temp_name
                    k1 = k1 + 1
            if k1 > 0:
                TE_Site_Name_TJ.loc[temp_site, "pd_domain"] = "BZFK_Right"




        # k = k + 1
        # if k > 0:
        #     break
    # print("TE_Site_Name_TJ = ",TE_Site_Name_TJ)

    TE_Site_Name_TJ.to_csv("./" + Group + "/" + Group + "_Goal_Site_TE_Name.csv", sep=',', header=True, index=True)
    folder_path0 = "./All_Group_TE_Site_And_Name"
    if not os.path.exists(folder_path0):
        os.mkdir(folder_path0)
    TE_Site_Name_TJ.to_csv("./All_Group_TE_Site_And_Name" + "/" + Group + "_Goal_Site_TE_Name.csv",sep=',',header=True,index=True)
    line1 = f1.readline()
f1.close()