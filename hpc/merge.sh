cd $VSC_HOME
OUTPUT_FILE="agglomerative_results_merged.csv"
head -1 agglomerative_array_results_0.csv > $OUTPUT_FILE
for i in {0..24}; do
    tail -n +2 agglomerative_array_results_${i}.csv >> $OUTPUT_FILE
done