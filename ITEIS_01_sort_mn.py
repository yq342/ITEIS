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

    M_S = pd.read_csv("./" + Group + "/" + Group + "_M_S.txt",sep='\t',header=None,index_col=None)
    S_M = pd.read_csv("./" + Group + "/" + Group + "_S_M.txt",sep='\t',header=None,index_col=None)
    M_S_eff = M_S[(M_S[2] >= 2000) & (M_S[3] >= 10) & (M_S[3] <= 90)]
    S_M_eff = S_M[(S_M[2] >= 2000) & (S_M[3] >= 10) & (S_M[3] <= 90)]
    M_S_sort = M_S_eff.sort_values(by=[0,1])
    S_M_sort = S_M_eff.sort_values(by=[0,1])

    M_S_sort.to_csv("./" + Group + "/" + Group + "_M_S_Sort.txt",sep='\t',header=False,index=False)
    S_M_sort.to_csv("./" + Group + "/" + Group + "_S_M_Sort.txt",sep='\t',header=False,index=False)

    # print("M_S_sort = ",M_S_sort)

    k2 = k2 + 1
    line1 = f1.readline()  # 以行的形式进行读取文件
f1.close()
