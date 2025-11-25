from features.mfcc_extractor import extract_mfcc

path = "../data/processed/happy"
import os

file = os.listdir(path)[0]
mfcc = extract_mfcc(os.path.join(path, file))

print("MFCC shape:", mfcc.shape)
