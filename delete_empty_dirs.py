import os
# script to remove empty directories and only keep .csv (data and clinical_data) files
# after downloading data from TCGA
for cancer in os.listdir("./data"):
    if len(os.listdir(f"./data/{cancer}")) == 0: # no longer needed (no longer making empty dirs)
        os.rmdir(f"./data/{cancer}")
    for file in os.listdir(f"./data/{cancer}"):
        if not file.endswith(".csv"):
            os.remove(f"./data/{cancer}/{file}")
