Capstone Project for CAP5510 - Bioinformatics

Comparison, Evaluation, and Analysis of Historical and Modern Secondary Structure Prediction Methods

This repository contains code and data used to complete this project. It is not a completely automated process, as many steps were done by hand.

Notable files are described below:

process_raw_data.py - Used to convert raw DSSP data into strings that could be entered in to web servers

nn_model.ipynb - Notebook forked from work done by Yasir Barlas. Trains neural network and evaluates its performance on CASP14 proteins

evaluate.py - Computes confusion matrices, which were then used to calculate accuracy, F1, and AUC

data/ - contains CSVs at various stages of the project

data/results/ - training logs and confusion matrices

All libraries used can be found in requirements.txt
