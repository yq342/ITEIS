import pandas as pd
import pysam
import re

def Yq_Excat_Blat_Res(input_Group, input_Num):
    yq_columns = ["match", "mismatch", "rep.match", "N_s", "Q_gap_count", "Q_gap_bases", "T_gap_count", "T_gap_bases",
                  "strand", "Q_name", "Q_size",
                  "Q_start", "Q_end", "T_name", "T_size", "T_start", "T_end", "block_count", "blockSizes", "qStarts",
                  "tStarts"]
    blat_res = pd.DataFrame(columns=yq_columns)

    inpufileName = "./" + input_Group + "/" + input_Group + "_All_TE_blat_Goal_seq_" + str(input_Num) + "_output.psl"
    f2 = open(inpufileName, 'r')
    line2 = f2.readline()
    k1 = 0
    while line2:
        if line2[-1] == '\n':
            TempLine2 = line2[0:-1]
        else:
            TempLine2 = line2
        Line_Split = TempLine2.split('\t')
        # print("Line_Split = ",Line_Split)
        k1 = k1 + 1
        if k1 >= 6:
            for temp in range(len(Line_Split)):
                if temp < 18:
                    blat_res.loc[k1, yq_columns[temp]] = Line_Split[temp]
                else:
                    blat_res.loc[k1, yq_columns[temp]] = Line_Split[temp][0:-1]
        line2 = f2.readline()
    f2.close()
    return blat_res


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
    print("Group = ", Group)

    Goal_Blat_res_1 = Yq_Excat_Blat_Res(Group, 1)
    Goal_Blat_res_2 = Yq_Excat_Blat_Res(Group, 2)

    # print("Goal_Blat_res_1 = ",Goal_Blat_res_1)
    # print("Goal_Blat_res_2 = ",Goal_Blat_res_2)
    Goal_Blat_res_1.to_csv("./" + Group + "/" + Group + "_All_TE_blat_Goal_seq_1_output", sep='\t', header=True,
                           index=None)
    Goal_Blat_res_2.to_csv("./" + Group + "/" + Group + "_All_TE_blat_Goal_seq_2_output", sep='\t', header=True,
                           index=None)
    line1 = f1.readline()
f1.close()

del Goal_Blat_res_1, Goal_Blat_res_2

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
    print("Group = ", Group)

    Goal_Read_Name_and_Goal_Site_TJ = pd.read_csv("./" + Group + "/" + Group + "_Read_Name_and_Goal_Site_TJ", sep='\t',
                                                  header=0, index_col=None)
    Goal_Blat_res_1 = pd.read_csv("./" + Group + "/" + Group + "_All_TE_blat_Goal_seq_1_output", sep='\t', header=0,
                                  index_col=None)
    Goal_Blat_res_2 = pd.read_csv("./" + Group + "/" + Group + "_All_TE_blat_Goal_seq_2_output", sep='\t', header=0,
                                  index_col=None)


    # Goal_Blat_res_1_eff_Map_TE_Right = Goal_Blat_res_1[(Goal_Blat_res_1["Q_start"]<=10)&(Goal_Blat_res_1["Q_end"]<=90)&(Goal_Blat_res_1["T_end"]>=Goal_Blat_res_1["T_size"]-10)]
    # Goal_Blat_res_1_eff_Map_TE_Left = Goal_Blat_res_1[(Goal_Blat_res_1["Q_start"]>=10)&(Goal_Blat_res_1["Q_end"]>=90)&(Goal_Blat_res_1["T_start"]<=10)]

    # Goal_Blat_res_2_eff_Map_TE_Right = Goal_Blat_res_2[(Goal_Blat_res_2["Q_start"]<=10)&(Goal_Blat_res_2["Q_end"]<=90)&(Goal_Blat_res_2["T_end"]>=Goal_Blat_res_2["T_size"]-10)]
    # Goal_Blat_res_2_eff_Map_TE_Left = Goal_Blat_res_2[(Goal_Blat_res_2["Q_start"]>=10)&(Goal_Blat_res_2["Q_end"]>=190)&(Goal_Blat_res_2["T_start"]<=10)]

    Goal_Blat_res_1_eff_Map_TE_Right = Goal_Blat_res_1[
        (Goal_Blat_res_1["Q_start"] <= 10) & (Goal_Blat_res_1["Q_end"] <= 90) & (
                    Goal_Blat_res_1["T_end"] >= Goal_Blat_res_1["T_size"] - 10)]
    Goal_Blat_res_1_eff_Map_TE_Left = Goal_Blat_res_1[
        (Goal_Blat_res_1["Q_start"] >= 10) & (Goal_Blat_res_1["Q_end"] >= 90) & (Goal_Blat_res_1["T_start"] <= 10)]

    Goal_Blat_res_2_eff_Map_TE_Right = Goal_Blat_res_2[
        (Goal_Blat_res_2["Q_start"] <= 10) & (Goal_Blat_res_2["Q_end"] <= 90) & (
                    Goal_Blat_res_2["T_end"] >= Goal_Blat_res_2["T_size"] - 10)]
    Goal_Blat_res_2_eff_Map_TE_Left = Goal_Blat_res_2[
        (Goal_Blat_res_2["Q_start"] >= 10) & (Goal_Blat_res_2["Q_end"] >= 90) & (Goal_Blat_res_2["T_start"] <= 10)]

    All_TE_Seq_Map_Q = pd.DataFrame()

    k1 = 0
    for temp_i in list(Goal_Blat_res_1_eff_Map_TE_Right.index):
        for temp_c in list(Goal_Blat_res_1_eff_Map_TE_Right.columns):
            All_TE_Seq_Map_Q.loc[k1, temp_c] = Goal_Blat_res_1_eff_Map_TE_Right.loc[temp_i, temp_c]
        All_TE_Seq_Map_Q.loc[k1, "Domain"] = "Right"
        k1 = k1 + 1

    for temp_i in list(Goal_Blat_res_1_eff_Map_TE_Left.index):
        for temp_c in list(Goal_Blat_res_1_eff_Map_TE_Left.columns):
            All_TE_Seq_Map_Q.loc[k1, temp_c] = Goal_Blat_res_1_eff_Map_TE_Left.loc[temp_i, temp_c]
        All_TE_Seq_Map_Q.loc[k1, "Domain"] = "Left"
        k1 = k1 + 1

    for temp_i in list(Goal_Blat_res_2_eff_Map_TE_Right.index):
        for temp_c in list(Goal_Blat_res_2_eff_Map_TE_Right.columns):
            All_TE_Seq_Map_Q.loc[k1, temp_c] = Goal_Blat_res_2_eff_Map_TE_Right.loc[temp_i, temp_c]
        All_TE_Seq_Map_Q.loc[k1, "Domain"] = "Right"
        k1 = k1 + 1

    for temp_i in list(Goal_Blat_res_2_eff_Map_TE_Left.index):
        for temp_c in list(Goal_Blat_res_2_eff_Map_TE_Left.columns):
            All_TE_Seq_Map_Q.loc[k1, temp_c] = Goal_Blat_res_2_eff_Map_TE_Left.loc[temp_i, temp_c]
        All_TE_Seq_Map_Q.loc[k1, "Domain"] = "Left"
        k1 = k1 + 1

    for temp_i in list(All_TE_Seq_Map_Q.index):
        Q_Name = All_TE_Seq_Map_Q.loc[temp_i, "Q_name"][0:-2]
        # print("Q_Name = ",Q_Name)
        temp_pd = Goal_Read_Name_and_Goal_Site_TJ[Goal_Read_Name_and_Goal_Site_TJ["reads_name"] == Q_Name]
        # print("temp_pd = ",temp_pd)
        goal_index = list(temp_pd.index)[0]
        All_TE_Seq_Map_Q.loc[temp_i, "Q_Site"] = temp_pd.loc[goal_index, "Site"]

    All_TE_Seq_Map_Q_Sort = All_TE_Seq_Map_Q.sort_values(by=["Q_Site", "T_name"])

    All_TE_Seq_Map_Q_Sort.to_csv("./" + Group + "/" + Group + "_Goal_Blat_res_eff_Map_TE.csv", sep=',', header=True,
                                 index=None)

    line1 = f1.readline()
f1.close()
