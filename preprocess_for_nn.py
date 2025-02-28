import pandas as pd
import os

# load csv
input_file = "data/predictions.csv"
output_file = "data/processed_for_nn_predictions.csv"

df = pd.read_csv(input_file, usecols=['ID', 'fixed', 'q3'])

MAX_LENGTH = 400

# df to store processed rows
processed_rows = []

for _, row in df.iterrows():
    seq_id = row['ID']
    fixed_seq = str(row['fixed'])  
    q3_seq = str(row['q3']).replace('B', 'E')  # Replace 'B' with 'E' to match labels
    
    # Split sequences into chunks of max length
    for i in range(0, len(fixed_seq), MAX_LENGTH):
        processed_rows.append({
            'ID': seq_id,
            'fixed': fixed_seq[i:i + MAX_LENGTH],
            'q3': q3_seq[i:i + MAX_LENGTH]
        })

# save to file
processed_df = pd.DataFrame(processed_rows)
processed_df.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")
