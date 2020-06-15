# tcgaEnrichr-Viewer

Apply patientcohortsEnrichr to TCGA

## Preparation

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Download RNA-seq and clinical data from TCGA database

```bash
source venv/bin/activate
python3 init.py
```
