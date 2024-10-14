#!/bin/bash

# Function to display help message
usage() {
    echo "Usage: $0 -i <InputFileName> -r <Refgenome_name> -l <readlength> -t <Ref_TE> -j <ITEIS_threads>"
    echo
    echo "Options:"
    echo "  -i    Input file name"
    echo "  -r    Reference genome name"
    echo "  -l    Length of reads"
    echo "  -t    Reference transposable elements (TE)"
    echo "  -j    Number of threads for ITEIS"
    exit 1
}

# Check if no arguments are provided
if [ "$#" -eq 0 ]; then
    usage
fi

# Parse command-line options
while getopts "i:r:l:t:j:h" opt; do
  case $opt in
    i)
      InputFileName=$OPTARG
      ;;
    r)
      Refgenome_name=$OPTARG
      ;;
    l)
      readlength=$OPTARG
      ;;
    t)
      Ref_TE=$OPTARG
      ;;
    j)
      ITEIS_threads=$OPTARG
      ;;
    h)
      usage
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

# Print the provided arguments
echo "Input File Name: $InputFileName"
echo "Reference Genome Name: $Refgenome_name"
echo "Read Length: $readlength"
echo "Reference TE: $Ref_TE"
echo "ITEIS Threads: $ITEIS_threads"
echo "$InputFileName" > All_File_Name


#InputFileName="os_chr3"
#Refgenome_name="os_chr3.fasta"
#readlength=100
#Ref_TE="All_TE.fasta"
#ITEIS_threads=16


# step 1 input fq file
if [ ! -d "./${InputFileName}" ]; then
     mkdir "./${InputFileName}"
fi
cd ./${InputFileName}
bwa index "../RefGenome/${Refgenome_name}"
 echo ${InputFileName}
bwa mem -t ${ITEIS_threads} -k 32 -M "../RefGenome/${Refgenome_name}" ../fastq/pirs_reads_100_180_1.fq ../fastq/pirs_reads_100_180_2.fq >"${InputFileName}_OS.sam"

samtools view -b -@ ${ITEIS_threads} "${InputFileName}_OS.sam" >"${InputFileName}_OS.bam"
samtools sort -@ ${ITEIS_threads} "${InputFileName}_OS.bam" >"${InputFileName}_OS_sort.bam"
samtools index -@ ${ITEIS_threads} "${InputFileName}_OS_sort.bam" >"${InputFileName}_OS_sort.bam.bai"
samtools view -@ ${ITEIS_threads} "${InputFileName}_OS.sam" | awk -F'\t' '{if($6 ~ /^([0-9]+)M([0-9]+)S/ ){print $3"\t"$4"\t"$4+gensub(/^([0-9]+)M([0-9]+)S.*$/, "\\1", "g", $6)"\t"gensub(/^([0-9]+)M([0-9]+)S.*$/, "\\1", "g", $6)"\t"$1}}' > "${InputFileName}_M_S.txt"
samtools view -@ ${ITEIS_threads} "${InputFileName}_OS.sam" | awk -F'\t' '{if($6 ~ /^([0-9]+)S([0-9]+)M/ ){print $3"\t"$4"\t"$4+gensub(/^([0-9]+)S([0-9]+)M.*$/, "\\2", "g", $6)"\t"gensub(/^([0-9]+)S([0-9]+)M.*$/, "\\2", "g", $6)"\t"$1}}' > "${InputFileName}_S_M.txt"
rm "${InputFileName}_OS.sam"
##################################################
cd ..
# Check if readlength equals 100 or 150
if [ "$readlength" -eq 100 ]; then
    python3 ITEIS_01_sort_mn.py
elif [ "$readlength" -eq 150 ]; then
    python3 ITEIS_01_sort.py
fi
cd ./${InputFileName}

#echo "ok0"

bedtools intersect -wa -wb -a "${InputFileName}_S_M_Sort.txt" -b "${InputFileName}_M_S_Sort.txt" >"${InputFileName}_S_M_Overlap_M_S"
echo "ok1"
cd ..
if [ "$readlength" -eq 100 ]; then
    python3 ITEIS_02_Overlap_Data_Ana_mn.py
elif [ "$readlength" -eq 150 ]; then
    python3 ITEIS_02_Overlap_Data_Ana.py
fi
cd ./${InputFileName}
#echo "ok02"
awk '{a[$0]++}END{for(i in a)if(a[i]>=5)print i}' "${InputFileName}_S_M_Overlap_M_S_Eff" > "${InputFileName}_S_M_Overlap_M_S_Eff_output_Dy5"
#echo "ok03"
cd ..
if [ "$readlength" -eq 100 ]; then
    python3 ITEIS_03_TE_Site_Excat_mn.py
elif [ "$readlength" -eq 150 ]; then
    python3 ITEIS_03_TE_Site_Excat.py
fi
cd ./${InputFileName}
#echo "ok04"

#cp "${InputFileName}_Goal_TE_Site" "../Diff_Group_TE_Site/${InputFileName}_Goal_TE_Site"
#echo "ok05"

#第二阶段
samtools fasta -@ ${ITEIS_threads} "${InputFileName}_OS_sort.bam" >"${InputFileName}_OS_sort.fasta"
#echo "ok06"
cd ..
if [ "$readlength" -eq 100 ]; then
    python3 ITEIS_04_Excat_TE_Site_Reads_mn.py
elif [ "$readlength" -eq 150 ]; then
    python3 ITEIS_04_Excat_TE_Site_Reads.py
fi
cd ./${InputFileName}
#echo "ok07"
sort "${InputFileName}_Insert_Site_Fq_Name" | uniq > "${InputFileName}_Insert_Site_Fq_Name_unique"
#echo "ok08"
sort "${InputFileName}_Insert_Site_Fq_Name_unique" | uniq | awk '{print $0"/1"}' > "${InputFileName}_Insert_Site_Fq_Name_unique_1_Name"
sort "${InputFileName}_Insert_Site_Fq_Name_unique" | uniq | awk '{print $0"/2"}' > "${InputFileName}_Insert_Site_Fq_Name_unique_2_Name"
#echo "ok09"

sort "${InputFileName}_Insert_Site_Fq_Name_unique_1_Name" > "${InputFileName}_Insert_Site_Fq_Name_unique_1_Name_sorted_file"
sort "${InputFileName}_Insert_Site_Fq_Name_unique_2_Name" > "${InputFileName}_Insert_Site_Fq_Name_unique_2_Name_sorted_file"
#echo "ok10"
seqtk subseq "${InputFileName}_OS_sort.fasta" "${InputFileName}_Insert_Site_Fq_Name_unique_1_Name_sorted_file" > "${InputFileName}_TE_eff_seq_1.fasta"
seqtk subseq "${InputFileName}_OS_sort.fasta" "${InputFileName}_Insert_Site_Fq_Name_unique_2_Name_sorted_file" > "${InputFileName}_TE_eff_seq_2.fasta"
#echo "ok11"

../bin/blat "../RefGenome/${Ref_TE}" "${InputFileName}_TE_eff_seq_1.fasta" "${InputFileName}_All_TE_blat_Goal_seq_1_output.psl"
../bin/blat "../RefGenome/${Ref_TE}" "${InputFileName}_TE_eff_seq_2.fasta" "${InputFileName}_All_TE_blat_Goal_seq_2_output.psl"
#echo "ok12"

cd ..
if [ "$readlength" -eq 100 ]; then
    python3 ITEIS_05_Excat_TE_mn.py
    python3 ITEIS_06_Excat_TE_name_mn.py
elif [ "$readlength" -eq 150 ]; then
    python3 ITEIS_05_Excat_TE.py
    python3 ITEIS_06_Excat_TE_name.py
fi
cd ./${InputFileName}
#echo "ok13"
