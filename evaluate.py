import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np

# load dataset
file_path = "data/predictions.csv"  
df = pd.read_csv(file_path, skip_blank_lines=True)
df.dropna(how="all", inplace=True)
print(len(df))

# mapping function for secondary structure characters
def map_q3_structure(seq):
    """Maps characters to standard Q3 classes (H, E, C)."""
    mapping = {'C': 'C', 'T': 'C', '-': 'C', 'c': 'C',  # coil
               'e': 'E', 'E': 'E', 'B': 'E',            # beta sheet
               'h': 'H', 'H': 'H'}             # alpha helix
    return ''.join([mapping.get(char, 'C') for char in seq])  # default to coil

# apply mapping 
df['q3'] = df['q3'].apply(map_q3_structure)
df['chou_fasman'] = df['chou_fasman'].apply(map_q3_structure)
df['gor'] = df['gor'].apply(map_q3_structure)
df['predator'] = df['predator'].apply(map_q3_structure)
df['jpred'] = df['jpred'].apply(map_q3_structure)

def total_confusion_matrix(y_true, y_pred):
    labels = ['H', 'E', 'C'] 
    total_cm = np.zeros((3, 3), dtype=int)  
    
    # iterate through sequences and accumulate confusion matrix counts
    for true_seq, pred_seq in zip(y_true, y_pred):
        cm = confusion_matrix(list(true_seq), list(pred_seq), labels=labels)
        total_cm += cm  # sum
    
    return total_cm

# generate confusion matrices for all methods
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