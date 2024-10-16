Identification of Transposable element insertion sites (ITEIS)
The Soft-cliped sequences were extracted from the alignment results to confirm the presence of new transposon insertion sites. 
The sequences corresponding to the positive or negative strands of the soft-clip sequences were extracted. Subsequently, 
the newly extracted sequences were re-aligned to the reference genome by using BWA (mem -t 4 -k 32 -M). The positions with 
target site duplication (TSD) was recorded after the realignment. Subsequently, the sequences were aligned to Ty3-retrotransposons. 
The transposon might have inserted into a new site if the sequences were aligned to both ends of the element (Fig. S2). In this study, 
to validate the model's reliability, 20 transposons were randomly selected from the established LTR-RT database and then randomly 
inserted into 100 positions on chromosome 3 of rice. The simulations of paired-end reads for all simulated chromosome 3 datasets 
were conducted using pIRS (simulate –l 100 –x 15) (Fan, 2012). For each dataset, simulated sequence reads were generated at 15x 
coverage depth. Subsequently, all insertion sites on chromosome 3 and the names of inserted transposons were obtained through 
sequence alignment. It was found that 82% of the sites could be accurately located by comparing the predicted values with the actual 
values, with identifiable transposon names detected at 79% of the insertion sites.
