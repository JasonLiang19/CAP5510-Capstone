import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np

# Load the dataset
file_path = "data/predictions.csv"  # Update with the correct path
df = pd.read_csv(file_path, skip_blank_lines=True)
df.dropna(how="all", inplace=True)
print(len(df))

# Mapping function for secondary structure characters
def map_q3_structure(seq):
    """Maps characters to standard Q3 classes (H, E, C)."""
    mapping = {'C': 'C', 'T': 'C', '-': 'C', 'c': 'C',  # Map to Coil
               'e': 'E', 'E': 'E', 'B': 'E',            # Map to Strand
               'h': 'H', 'H': 'H'}             # Map to Helix
    return ''.join([mapping.get(char, 'C') for char in seq])  # Default to Coil

# Apply mapping to all sequences
df['q3'] = df['q3'].apply(map_q3_structure)
df['chou_fasman'] = df['chou_fasman'].apply(map_q3_structure)
df['gor'] = df['gor'].apply(map_q3_structure)
df['predator'] = df['predator'].apply(map_q3_structure)
df['jpred'] = df['jpred'].apply(map_q3_structure)

# Define a function to compute the total confusion matrix
def total_confusion_matrix(y_true, y_pred):
    labels = ['H', 'E', 'C']  # Standard Q3 categories
    total_cm = np.zeros((3, 3), dtype=int)  # Initialize a 3x3 matrix with zeros
    
    # Iterate through all sequences and accumulate confusion matrix counts
    for true_seq, pred_seq in zip(y_true, y_pred):
        cm = confusion_matrix(list(true_seq), list(pred_seq), labels=labels)
        total_cm += cm  # Sum up across all sequences
    
    return total_cm

# Generate confusion matrices for all methods
methods = ['chou_fasman', 'gor', 'predator', 'jpred']

for method in methods:
    cm = total_confusion_matrix(df['q3'], df[method])
    
    # Plot the confusion matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['H', 'E', 'C'], yticklabels=['H', 'E', 'C'])
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title(f"Confusion Matrix: {method} vs Q3")
    plt.plot()
    plt.savefig(f'data/results/{method}_matrix.png')