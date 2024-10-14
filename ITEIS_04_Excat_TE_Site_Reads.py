import pandas as pd
import pysam
import re


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

    Read_Name_and_Goal_Site_TJ = pd.DataFrame(columns=["reads_name","Site"])
    k2 = 0
    fout = open("./" + Group + "/" + Group + "_Insert_Site_Fq_Name","w")
    Temp_Goal_Site = pd.read_csv("./" + Group + "/" + Group + "_Goal_TE_Site",sep='\t',header=0,index_col=None)
    #print("Temp_Goal_Site = ",Temp_Goal_Site)
    samfile = pysam.AlignmentFile("./" + Group + "/" + Group + "_OS_sort.bam", "rb")
    for yq_i in list(Temp_Goal_Site.index):
        Goal_Chr = Temp_Goal_Site.loc[yq_i,'0']
        Goal_Start = Temp_Goal_Site.loc[yq_i,'1']
        Goal_End = Temp_Goal_Site.loc[yq_i,'2']
        #print("Goal_Chr = ",Goal_Chr)
        #print("Goal_Start = ",Goal_Start)
        #print("Goal_End = ",Goal_End)

        reads = samfile.fetch(Goal_Chr, Goal_Start, Goal_End)

        Is_Eff = True
        Is_inset_letter = False
        cox = 0
        for read in reads:
            # print("read = ", read)
            try:
                # print(read)

                start_pos = read.reference_start + 1
                end_pos = read.reference_end + 1
                # print("start_pos = \n",start_pos)
                # print("end_pos = \n",end_pos)

                cigar = read.cigarstring
                # if ("S" in cigar) & ("M" in cigar) & (cigar.count("S") == 1) & (cigar.count("M") == 1):
                if ("S" in cigar) & ("M" in cigar):
                    # print(read)
                    read_name = read.query_name
                    #print(read_name)
                    fout.write(read_name)
                    fout.write("\n")
                    Read_Name_and_Goal_Site_TJ.loc[k2,"reads_name"] = read_name
                    Read_Name_and_Goal_Site_TJ.loc[k2,"Site"] = Goal_Chr + "_" + str(Goal_Start) + "_" + str(Goal_End)
                    k2 = k2 + 1
            except:
                pass
    fout.close()
    Read_Name_and_Goal_Site_TJ.to_csv("./" + Group + "/" + Group + "_Read_Name_and_Goal_Site_TJ",sep='\t',header=True,index=False)

    line1 = f1.readline()
f1.close()
