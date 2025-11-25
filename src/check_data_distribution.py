import os

root = "../data/processed"

for emo in os.listdir(root):
    f = os.path.join(root, emo)
    if os.path.isdir(f):
        print(emo, ":", len(os.listdir(f)), "files")
