import boto3
from botocore.exceptions import ClientError
import logging
import config
import os
import csv

def upload_file(local_file, object_name=None):
    """Upload a file to the S3 bucket for this project

    :param local_file: Path to local file to upload
    :param object_name: Name under which to store the file in the bucket
    :return: True if file is uploaded, else False
    """
    if (object_name == None):
        object_name = local_file
    try:
        s3 = boto3.client('s3', aws_access_key_id=config.ACCESS_KEY,
                      aws_secret_access_key=config.SECRET_KEY)
        s3.upload_file(
            local_file, config.BUCKET, object_name
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(object_name, location = None):

    """Download a file from the S3 bucket for this project

    :param object_name: Name under which the file is stored in the bucket
    :param location: Local path to which the file is downloaded
    :return: True if file is downloaded, else False
    """
    if (object_name == None):
        object_name = local_file
    try:
        s3 = boto3.client('s3', aws_access_key_id=config.ACCESS_KEY,
                          aws_secret_access_key=config.SECRET_KEY)
        if (location == None):
            location = "./" + object_name
        s3.download_file(
            config.BUCKET, object_name, location
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True

# upload data
uploaded_cancers = []
for cancer in os.listdir("./data"):
    if (cancer == ".DS_Store"): continue
    try:
        upload_file(f"./data/{cancer}/data.csv", f"{cancer}_data.csv")
        upload_file(f"./data/{cancer}/clinical_data.csv", f"{cancer}_clinical_data.csv")
        uploaded_cancers.append(cancer)
        print(cancer)
    except FileNotFoundError as e:
        print(e)
        continue

# save a .csv with cancer names
with open("./uploaded_cancers", 'w', newline='') as out_file:
     wr = csv.writer(out_file, quoting=csv.QUOTE_ALL)
     wr.writerow(uploaded_cancers)



# upload_file("./data.csv", "data.csv")
# upload_file("./clinical_data.csv", "clinical_data.csv")
