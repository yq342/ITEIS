import pandas as pd
import pysam
import re

pattern = re.compile(r'^(\d+M(\d{2,}|[1-9]\d*)I\d+M)$')

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

    Temp_Goal_Site = pd.read_csv("./" + Group + "/" + Group + "_S_M_Overlap_M_S_Eff_output_Dy5",sep='\t',header=None,index_col=None)
    # print("Temp_Goal_Site = ",Temp_Goal_Site)
    samfile = pysam.AlignmentFile("./" + Group + "/" + Group + "_OS_sort.bam", "rb")
    for yq_i in list(Temp_Goal_Site.index):

        Goal_Chr = Temp_Goal_Site.loc[yq_i,0]
        Goal_Start = Temp_Goal_Site.loc[yq_i,1]
        Goal_End = Temp_Goal_Site.loc[yq_i,2]
        print("Goal_Chr = ",Goal_Chr)
        print("Goal_Start = ",Goal_Start)
        print("Goal_End = ",Goal_End)

        reads = samfile.fetch(Goal_Chr, Goal_Start, Goal_End)


        Is_Eff = True
        Is_inset_letter = False
        cox = 0
        for read in reads:
            # print("read = ", read)
            try:
                print(read)

                start_pos = read.reference_start + 1
                end_pos = read.reference_end + 1
                print("start_pos = ",start_pos)
                print("end_pos = ",end_pos)

                cigar = read.cigarstring
                print("cigar = ", cigar)

                is_100M = False
                if cigar is not None:
                    if "100M" in cigar:
                        is_100M = True
                match = pattern.match(cigar)
                if match:

                    Is_inset_letter = True
                print("Is_inset_letter = ", Is_inset_letter)

                if is_100M:

                    # print("start_pos = ",start_pos)
                    # print("end_pos = ",end_pos)
                    # print("Goal_Start = ",Goal_Start)
                    if Goal_End < (end_pos + start_pos) / 2:

                        if (Goal_Start - start_pos) < 3:
                            pass
                        else:
                            Is_Eff = False
                    elif ((end_pos + start_pos) / 2) < Goal_Start:
                        if (end_pos - Goal_End) < 3:
                            pass
                        else:
                            Is_Eff = False
                    else:
                        Is_Eff = False

                    # Is_Eff = True
                    # print("Is_Eff = ",Is_Eff)

                if Is_Eff:
                    pass
                else:
                    break
            except:
                pass
            if "H" not in cigar:
                cox = cox + 1
            if cox >= 20:
                Is_Eff = False


        Temp_Goal_Site.loc[yq_i,"is_eff"] = Is_Eff
        Temp_Goal_Site.loc[yq_i,"Is_inset_letter"] = Is_inset_letter
        # 关闭SAM文件
    samfile.close()
    Goal_Site = Temp_Goal_Site[Temp_Goal_Site["is_eff"]]
    # print("Goal_Site = ",Goal_Site)
    Goal_Site.to_csv("./" + Group + "/" + Group + "_Goal_TE_Site",sep='\t',header=True,index=None)

    line1 = f1.readline()
f1.close()
