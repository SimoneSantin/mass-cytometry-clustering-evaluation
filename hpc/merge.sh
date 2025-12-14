cd $VSC_HOME
OUTPUT_FILE="flowsom_results_merged.csv"
head -1 flowsom_array_results_0.csv > $OUTPUT_FILE
for i in {0..24}; do
    tail -n +2 flowsom_array_results_${i}.csv >> $OUTPUT_FILE
done

OUTPUT_FILE="phenograph_results_merged.csv"
head -1 phenograph_array_results_0.csv > $OUTPUT_FILE
for i in {0..24}; do
    tail -n +2 phenograph_array_results_${i}.csv >> $OUTPUT_FILE
done

echo "Unione completata in $OUTPUT_FILE"
