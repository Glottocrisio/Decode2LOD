import requests
import json
import time
from typing import List, Dict

BASE_URL = "https://de-crypt.org/decrypt-web/api"

def fetch_records(table: str, page: int = 1, page_size: int = 100) -> Dict:
    """Fetch a page of records from the API."""
    url = f"{BASE_URL}/list/{table}"
    params = {
        "page": page,
        "page_size": page_size
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_all_records(table: str) -> List[Dict]:
    """Fetch all records from the API, handling pagination."""
    all_records = []
    page = 1
    while page < 4026:
        print(f"Fetching page {page}...")
        data = fetch_records(table, page)
        records = data.get('records', [])
        all_records.extend(records)

        page += 1
        #time.sleep(1) 
    
    return all_records

def fetch_specific_record(table: str, record_id: str) -> Dict:
    """Fetch a specific record by its ID."""
    url = f"{BASE_URL}/view/{table}/{record_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_all_record_details(table: str, records: List[Dict]) -> List[Dict]:
    """Fetch detailed information for all records."""
    detailed_records = []
    total_records = len(records)
    
    for index, record in enumerate(records, start=1):
        record_id = record.get('id')
        if record_id:
            print(f"Fetching details for record {record_id} ({index}/{total_records})...")
            try:
                detailed_record = fetch_specific_record(table, record_id)
                detailed_records.append(detailed_record)
                #time.sleep(1)  
            except requests.RequestException as e:
                print(f"Error fetching record {record_id}: {e}")
        else:
            print(f"Skipping record at index {index} due to missing ID")
    
    return detailed_records

def save_to_json(data: List[Dict], filename: str):
    """Save the data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    table = "records"
    summary_filename = "decode_records_summary.json"
    detailed_filename = "decode_records_detailed.json"
    
    try:
        # print(f"Fetching all records from the '{table}' table...")
        # records_summary = fetch_all_records(table)
        # print(f"Fetched {len(records_summary)} record summaries.")
        
        # print(f"Saving record summaries to {summary_filename}...")
        # save_to_json(records_summary, summary_filename)
        
        records_summary = fetch_all_records(table)
        print("Fetching detailed information for each record...")
        detailed_records = fetch_all_record_details(table, records_summary)
        print(f"Fetched details for {len(detailed_records)} records.")
        
        print(f"Saving detailed records to {detailed_filename}...")
        save_to_json(detailed_records, detailed_filename)
        
        print("Done!")
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")

if __name__ == "__main__":
    main()