import requests
import re
import json
import subprocess
import pandas as pd
import os
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_case(file_id, dir, retry_count=5, backoff_factor=2):
    # data_endpt = "https://api.gdc.cancer.gov/data/{}".format(file_id)

    # response = requests.get(data_endpt, headers = {"Content-Type": "application/json"})

    # # The file name can be found in the header within the Content-Disposition key.
    # response_head_cd = response.headers["Content-Disposition"]

    # file_name = re.findall("filename=(.+)", response_head_cd)[0]
    # file_dir = os.path.join(dir, file_name)

    # with open(file_dir, "wb") as output_file:
    #     output_file.write(response.content)
    data_endpt = f"https://api.gdc.cancer.gov/data/{file_id}"
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=retry_count,  # Number of retries
        backoff_factor=backoff_factor,  # Exponential backoff
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP errors
        raise_on_status=False
    )
    
    # Attach the retry strategy to the session
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)

    try:
        # Set headers and make the GET request with streaming
        response = http.get(data_endpt, headers={"Content-Type": "application/json"}, stream=True, timeout=(10, 60))

        # Raise an error for bad responses (4XX or 5XX status codes)
        response.raise_for_status()

        # Extract the filename from the Content-Disposition header
        response_head_cd = response.headers.get("Content-Disposition", "")
        file_name = re.findall("filename=(.+)", response_head_cd)[0]

        # Build the full path to save the file
        file_dir = os.path.join(dir, file_name)

        # Stream the response content to the file in chunks to avoid memory overload
        with open(file_dir, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive chunks
                    output_file.write(chunk)

        print(f"File {file_name} downloaded successfully to {file_dir}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_data(dataset_type):
    manifest_df = pd.read_csv(f'manifest_{dataset_type}_filtered.csv', sep=',')

    #   Check if required columns are present
    if 'id' not in manifest_df.columns:
        raise ValueError("Manifest file must contain an 'id' column for file_id")

    ids = []
    # Iterate over the DataFrame rows
    for i, (index, row) in enumerate(manifest_df.iterrows()):
        ids.append({'id': row['id'], 'filename':row['filename']})

    directory = f'{dataset_type}_dataset'
    os.makedirs(directory, exist_ok=True)

    for item in ids:
        # Construct the full file path
        file_path = os.path.join(directory, item['filename'])
        

        # Check if the file exists
        if os.path.isfile(file_path):
            print("we skip: ", item['filename'])
            continue
        else:
            print("we obtain: ", item['filename'])
            get_case(item['id'], directory)

    
def read_slide_ids_from_csv(file_path):
    """
    Reads all items from the 'slide_id' column of the CSV file and returns them as a list.
    """
    slide_ids = []
    train_file = os.path.join(file_path, 'train.csv')
    with open(train_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            slide_ids.append(row['slide_id'])


    test_file = os.path.join(file_path, 'test.csv')
    with open(test_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            slide_ids.append(row['slide_id'])
    
    print(len(slide_ids))

    return slide_ids


def filter_by_filename(dataset, file_path_slides):
    slide_ids = read_slide_ids_from_csv(file_path_slides)
    input_file = f'manifest_{dataset}.txt' 
    output_file = f'manifest_{dataset}_filtered_first.csv' 
    output_file2 = f'manifest_{dataset}_filtered.csv' 

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        # Initialize a CSV writer for the output file
        csv_writer = csv.writer(outfile)

        # Read the input file as a tab-delimited file
        for i, line in enumerate(infile):
            # Split the line by tab to get the columns
            columns = line.strip().split('\t')

            # Write the header row (first line) to the CSV file
            if i == 0:
                csv_writer.writerow(columns)
            else:
                # Check if the filename contains 'DX'
                if 'DX' in columns[1] and '.svs' in columns[1]:  # filename is the second column
                    # Write the filtered row to the CSV file
                    csv_writer.writerow(columns)
    
    with open(output_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        rows_to_keep = [row for row in reader if row['filename'].replace('.svs', '') in slide_ids]

    print(len(rows_to_keep))
    assert len(rows_to_keep) == len(slide_ids)
        
    # Write filtered rows to a new CSV file
    with open(output_file2, mode='w', newline='') as file:
        if rows_to_keep:
            fieldnames = rows_to_keep[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_to_keep) 



def main():
    # CHANGE params!!
    dataset = 'blca'
    file_path_slides = "../MMP/src/splits/survival/TCGA_BLCA_overall_survival_k=0"

    # filter_by_filename(dataset, file_path_slides)
    get_data(dataset)
    # rm_processed_slides(dataset)


if __name__ == '__main__':
    main()