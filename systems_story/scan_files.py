#!/usr/bin/env python3
"""
Script to scan all files on the machine and collect metadata into a dictionary.
Scans from the root directory (/) recursively.
"""

import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
home = Path.home()

def _is_excluded(path, exclude_paths):
    for excluded in exclude_paths:
        try:
            if os.path.commonpath([path, excluded]) == excluded:
                return True
        except ValueError:
            continue
    return False


def scan_filesystem(start_path="/", exclude_paths=None):
    """
    Scans the filesystem starting from start_path and collects file metadata.
    
    Args:
        start_path: Root directory to start scanning from (default: "/")
        exclude_paths: List of absolute paths to exclude from scanning
    
    Returns:
        Dictionary with file metadata: {path: {filename, extension, size}}
    """
    files_data = {}
    exclude_paths = [os.path.abspath(p) for p in (exclude_paths or [])]
    
    for root, dirs, files in os.walk(start_path):
        abs_root = os.path.abspath(root)

        if _is_excluded(abs_root, exclude_paths):
            dirs[:] = []
            continue

        # Remove directories that typically have permission issues or are unnecessary
        dirs[:] = [
            d for d in dirs
            if d not in ['.Trash', '.Spotlight-V100', '.TemporaryItems']
            and not _is_excluded(os.path.join(abs_root, d), exclude_paths)
        ]
        
        for filename in files:
            try:
                filepath = os.path.join(root, filename)
                
                # Get file stats
                stat = os.stat(filepath)
                size = stat.st_size
                
                # Get file extension
                _, extension = os.path.splitext(filename)
                
                # Get creation/modification timestamp
                # On macOS, use st_birthtime (creation time) if available, otherwise use st_mtime
                if hasattr(stat, 'st_birthtime'):
                    # macOS creation time
                    timestamp = stat.st_birthtime
                    timestamp_type = 'created'
                else:
                    # Fallback to modification time on other systems
                    timestamp = stat.st_mtime
                    timestamp_type = 'modified'
                
                # Convert timestamp to readable format
                timestamp_readable = datetime.fromtimestamp(timestamp).isoformat()
                
                # Store in dictionary
                files_data[filepath] = {
                    'filename': filename,
                    'extension': extension if extension else 'no_extension',
                    'size': size,
                    'path': filepath,
                    'timestamp': timestamp,
                    'timestamp_readable': timestamp_readable,
                    'timestamp_type': timestamp_type
                }
                
            except (OSError, PermissionError) as e:
                # Skip files we can't access
                continue
    
    return files_data


def print_summary(files_data):
    """Print a summary of the scan results."""
    print(f"\nTotal files found: {len(files_data)}")
    
    # Calculate total size
    total_size = sum(f['size'] for f in files_data.values())
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    
    # Count by extension
    extensions = defaultdict(int)
    for f in files_data.values():
        extensions[f['extension']] += 1
    
    print(f"\nTop 10 file extensions:")
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {ext}: {count}")


def sort_files_by_size(files_data, descending=True):
    """Return a list of file metadata sorted by size."""
    return sorted(files_data.values(), key=lambda f: f["size"], reverse=descending)


if __name__ == "__main__":
    print("Scanning filesystem... This may take a while...")
    print("Press Ctrl+C to stop.\n")
    
    try:
        exclude_paths = [
            "/usr/bin",
        ]
        files_dict = scan_filesystem(home, exclude_paths=exclude_paths)
        print_summary(files_dict)

        files_sorted = sort_files_by_size(files_dict, descending=True)
        
        # Save to a file for later analysis
        import json
        with open("files_scan_results.json", "w") as f:
            # Convert the dict to JSON-serializable format
            json_data = files_sorted[:10000]  # Sample of largest files
            json.dump(json_data, f, indent=2)
        
        print(f"\nSample of results saved to 'files_scan_results.json'")
        print(f"Full results stored in 'files_dict' variable with {len(files_dict)} files")
        
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.")
        print(f"Files scanned so far: {len(files_dict) if 'files_dict' in locals() else 0}")
