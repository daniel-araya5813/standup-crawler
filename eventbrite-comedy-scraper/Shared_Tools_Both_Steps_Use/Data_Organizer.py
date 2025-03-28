"""
Data organization tools used by both steps of the application.
"""

import csv
import logging
from typing import Dict, List, Set, Any

def is_duplicate_value(value: str, seen_values: Set[str]) -> bool:
    """
    Check if a value has already been seen.
    
    Args:
        value (str): The value to check
        seen_values (Set[str]): Set of values that have already been seen
        
    Returns:
        bool: True if the value is a duplicate, False otherwise
    """
    if not value:
        return False
    
    normalized_value = value.lower().strip()
    return normalized_value in seen_values

def is_complete_record(record: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Check if a record has all required keys with non-empty values.
    
    Args:
        record (Dict[str, Any]): The record to check
        required_keys (List[str]): List of required keys
        
    Returns:
        bool: True if all required keys have non-empty values
    """
    for key in required_keys:
        if key not in record or not record[key]:
            return False
    return True

def save_records_to_csv(records: List[Dict[str, Any]], filename: str, fieldnames: List[str] = None) -> None:
    """
    Save a list of records to a CSV file.
    
    Args:
        records (List[Dict[str, Any]]): List of record dictionaries
        filename (str): Path to the output CSV file
        fieldnames (List[str], optional): List of field names for the CSV header
                                         If None, uses keys from the first record
    """
    if not records:
        logging.warning("⚠️ No records to save.")
        return
    
    # Determine field names if not provided
    if fieldnames is None:
        fieldnames = list(records[0].keys())
    
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        
        logging.info(f"💾 Saved {len(records)} records to '{filename}'")
    except Exception as e:
        logging.error(f"❌ Error writing to CSV file: {e}")

def read_csv_to_records(filename: str) -> List[Dict[str, str]]:
    """
    Read records from a CSV file.
    
    Args:
        filename (str): Path to the CSV file
        
    Returns:
        List[Dict[str, str]]: List of record dictionaries
    """
    records = []
    
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append(row)
        
        logging.info(f"📊 Read {len(records)} records from '{filename}'")
    except FileNotFoundError:
        logging.error(f"❌ CSV file not found: {filename}")
    except Exception as e:
        logging.error(f"❌ Error reading CSV file: {e}")
    
    return records

def merge_csv_files(input_files: List[str], output_file: str, dedup_key: str = None) -> None:
    """
    Merge multiple CSV files into one, with optional deduplication.
    
    Args:
        input_files (List[str]): List of input CSV file paths
        output_file (str): Path to the output CSV file
        dedup_key (str, optional): Field name to use for deduplication
    """
    all_records = []
    seen_values = set()
    
    for file in input_files:
        records = read_csv_to_records(file)
        
        if dedup_key:
            # Add only non-duplicate records
            for record in records:
                if dedup_key in record and not is_duplicate_value(record[dedup_key], seen_values):
                    all_records.append(record)
                    if record[dedup_key]:
                        seen_values.add(record[dedup_key].lower().strip())
        else:
            # Add all records without deduplication
            all_records.extend(records)
    
    if all_records:
        # Use fieldnames from the first record
        fieldnames = list(all_records[0].keys())
        save_records_to_csv(all_records, output_file, fieldnames)
    else:
        logging.warning("⚠️ No records to save after merging.")