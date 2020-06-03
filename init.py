# Script to acquire RNA-Seq data from TCGA and compile it into a single .csv
# for further processing.
import requests
import json
import os
import re
import gzip
import shutil
import tarfile
import pathlib
import pandas as pd

# Retrieve data from the TCGA API

# Endpoints
base_url = 'https://api.gdc.cancer.gov/'
files_endpt = base_url + 'files/'
genes_endpt = base_url + 'genes/'
cases_endpt = base_url + 'cases/'
data_endpt = base_url + "data/"

# data type of files we want
data_type = "htseq.counts"

# The 'fields' parameter is passed as a comma-separated string of single names.
# fields = [""]
# fields = ','.join(fields)

# filter files for only RNA-Seq results
filters = {
    "op": "and",
     "content":[
         {
            "op": "in",
            "content":
             {
                 "field": "files.experimental_strategy",
                 "value": ["RNA-Seq"],
             }
         },
         {
            "op": "in",
            "content":
             {
                 "field": "access",
                 "value": ["open"],

             }
         },

     ],
}

# build parameters object
params = {
    "filters": json.dumps(filters)
}

# get list of all files with RNA-seq results
response = requests.get(files_endpt, params = params) # optionally also provide params argument
data = json.loads(response.content.decode("utf-8"))

# get list of results
results = data["data"]["hits"]
results = filter(lambda x: data_type in x["file_name"], results)
file_uuid_list = [ entry["file_id"] for entry in results]

params = {"ids": file_uuid_list}

# A POST is used, so the filter parameters can be passed directly as a Dict object.
response = requests.post(data_endpt,
                        data = json.dumps(params),
                        headers={
                            "Content-Type": "application/json"})

# filename is found in the Content-Disposition header of response
response_head_cd = response.headers["Content-Disposition"]
file_name = re.findall("filename=(.+)", response_head_cd)[0]

downloads_folder = "TCGA_downloads/"

# Save .tar.gz zipped file to TCGA_downloads folder
with open(downloads_folder + file_name, "wb") as f_out:
    f_out.write(response.content)

# extract the root tar archive
tar = tarfile.open(downloads_folder + file_name, "r:gz")
tar.extractall("./{}".format(downloads_folder))
folder = file_name.split(".tar.gz")[0]

for tarinfo in tar:
    if (tarinfo.name == "MANIFEST.txt"): continue
    file_id = tarinfo.name.split("/")[0]
    # unzip inner .gz files
    with gzip.open(downloads_folder + tarinfo.name, "rb") as f_in:
        with open("data/{}.txt".format(file_id), "wb") as f_out:
            f_out.write(f_in.read())
tar.close()

# initialize empty df
df = pd.DataFrame({"gene": []})
df = df.set_index("gene")

# loop over files, merging with pre-existing data
for file in pathlib.Path('data').glob('*.txt'):
    with open(file, "rb") as f_in:
        new_df = pd.read_csv(f_in, sep = "\t", header = None)
        file_id = re.findall("data/(.+).txt", f_in.name)[0]
        new_df.columns = ["gene", file_id]
        new_df = new_df.set_index("gene")
        df = pd.DataFrame.merge(df, new_df, how="outer", left_on = "gene", right_on = "gene")

# export to the data directory
df.to_csv('data.csv', encoding='utf-8')
