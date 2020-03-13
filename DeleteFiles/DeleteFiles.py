import os
import shutil

for root, subdirs, files in os.walk(r"O:\Data\OND01\Raw_data"):
    for d in subdirs:
        if d == "Analyzed":
            shutil.rmtree(os.path.join(root, d))




