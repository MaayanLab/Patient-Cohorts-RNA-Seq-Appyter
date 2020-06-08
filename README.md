# tcgaEnrichr-Viewer

Apply patientcohortsEnrichr to TCGA

## Preparation

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Download RNA-seq data from TCGA database

```bash
source venv/bin/activate
mkdir data
mkdir TCGA_downloads
python3 init.py
```

The resulting .csv has the format:

gene, counts for file_id_1, counts for file_id_2, counts for file_id_3...

where each file_id is the UUID for the file in the TCGA database, and
can be mapped to other data (such as the case).
