import pandas as pd
import re

# load dataset
file_path = "raw_data.csv" 
df = pd.read_csv(file_path)

# extract necessary columns
df = df[['pdb', 'aa', 'q3']]
df.columns = ['ID', 'original', 'q3']

# remove entries with ID '7BGL', explanation in paper 
df = df[df['ID'] != '7BGL']

# group by ID and concatenate sequences
df = df.groupby('ID').agg({'original': ''.join, 'q3': ''.join}).reset_index()

# Apply lambda function to replace lowercase letters and '!' with 'X'
df['original'] = df['original'].apply(lambda seq: re.sub(r'[a-z!]', 'X', seq))

# Function to find the first repeating occurrence of the first 20 bases
def find_truncation_index(sequence):
    """Finds where the first 20 amino acid bases start repeating in the sequence."""
    if len(sequence) < 20:
        return len(sequence)  # If sequence is too short, return full length

    first_20 = sequence[:20]  # Extract first 20 amino acids
    next_occurrence = sequence.find(first_20, 20)  # Look for the next occurrence

    return next_occurrence if next_occurrence != -1 else len(sequence)

# Apply this function only to protein ID "6VR4"
for index, row in df.iterrows():
    seq = row['original']
    trunc_index = find_truncation_index(seq)  # Get truncation index

    # Truncate both sequence and q3 using the determined index
    df.at[index, 'original'] = seq[:trunc_index]
    df.at[index, 'q3'] = row['q3'][:trunc_index]

# define max sequence length (800 on JPRED site)
max_length = 800

sectioned_data = []
# Process each sequence to ensure max length of 1000 per section
for _, row in df.iterrows():
    seq_id = row['ID']
    sequence = row['original']
    q3_structure = row['q3']
    
    # Break sequences into chunks of max_length
    for i in range(0, len(sequence), max_length):
        section_number = (i // max_length) + 1  # Section count
        sectioned_data.append({
            'ID': seq_id,
            'section': section_number,
            'original': sequence[i:i+max_length],
            'q3': q3_structure[i:i+max_length]
        })

# Convert to dataframe
df_final = pd.DataFrame(sectioned_data)

# Save the processed dataset
output_path = "data/processed_dataset.csv"
df_final.to_csv(output_path, index=False)

print(f"Processed dataset saved as: {output_path}")
