import pandas as pd
f1 = open("All_File_Name", 'r')
line1 = f1.readline()  # 以行的形式进行读取文件
k2 = 0
yq_Time_set = []
while line1:
    if line1[-1] == '\n':
        TempLine1 = line1[0:-1]
    else:
        TempLine1 = line1
    Group = TempLine1
    print("Group = ",Group)


    HZE_S_M_Overlap_M_S = pd.read_csv("./" + Group + "/" + Group + "_S_M_Overlap_M_S",sep='\t',header=None,index_col=None)
    # print("R150H1_G_S_M_Overlap_M_S = \n",R150H1_G_S_M_Overlap_M_S)
    #  0     1       2       3                       4                     5      6      7      8                   9
    #chr06   8849079 8849182 103     A00192:118:H5YHLDSXX:2:1158:11993:13150 chr06   8848948 8849082 134     A00192:118:H5YHLDSXX:2:2529:12888:20181
    HZE_S_M_Overlap_M_S["overlap_len"] = HZE_S_M_Overlap_M_S[7]-HZE_S_M_Overlap_M_S[1]
    HZE_S_M_Overlap_M_S_Eff = HZE_S_M_Overlap_M_S[(HZE_S_M_Overlap_M_S["overlap_len"] < 20) & (HZE_S_M_Overlap_M_S["overlap_len"] > 1)]
    # print("R150H1_G_S_M_Overlap_M_S_Eff = ", R150H1_G_S_M_Overlap_M_S_Eff)
    new_overlap_site_Data = pd.DataFrame()
    new_overlap_site_Data[0] = HZE_S_M_Overlap_M_S_Eff[0]
    new_overlap_site_Data[1] = HZE_S_M_Overlap_M_S_Eff[1]
    new_overlap_site_Data[2] = HZE_S_M_Overlap_M_S_Eff[7]
    new_overlap_site_Data.to_csv("./" + Group + "/" + Group + "_S_M_Overlap_M_S_Eff",sep='\t',header=None,index=None)


    line1 = f1.readline()  # 以行的形式进行读取文件
f1.close()
