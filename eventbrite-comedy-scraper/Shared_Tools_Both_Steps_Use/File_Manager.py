"""
File handling tools used by both steps of the application.
"""

import os
import glob
from typing import Optional, List
import logging
import datetime

def ensure_directory_exists(directory_path: str) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        directory_path (str): Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logging.info(f"📁 Created directory: {directory_path}")

def find_newest_file(directory: str, prefix: str = "", suffix: str = ".csv") -> Optional[str]:
    """
    Find the newest file in a directory that matches the given prefix and suffix.
    
    Args:
        directory (str): Directory to search in
        prefix (str): File name prefix to match
        suffix (str): File extension to match
        
    Returns:
        Optional[str]: Path to the newest file, or None if no files found
    """
    ensure_directory_exists(directory)
    
    # Generate search pattern
    pattern = os.path.join(directory, f"{prefix}*{suffix}")
    
    # Find all matching files
    files = glob.glob(pattern)
    
    if not files:
        return None
    
    # Return the most recently modified file
    return max(files, key=os.path.getmtime)

def find_files_by_date(directory: str, date_str: str, suffix: str = ".csv") -> List[str]:
    """
    Find files created on a specific date.
    
    Args:
        directory (str): Directory to search in
        date_str (str): Date string in YYYY-MM-DD format
        suffix (str): File extension to match
        
    Returns:
        List[str]: List of matching file paths
    """
    ensure_directory_exists(directory)
    
    # Generate search pattern
    pattern = os.path.join(directory, f"*{date_str}*{suffix}")
    
    # Return all matching files
    return glob.glob(pattern)

def get_today_str() -> str:
    """
    Get today's date as a string in YYYY-MM-DD format.
    
    Returns:
        str: Today's date string
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")

def append_timestamp(filename: str) -> str:
    """
    Append a timestamp to a filename.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Filename with timestamp
    """
    name, ext = os.path.splitext(filename)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{name}_{timestamp}{ext}"