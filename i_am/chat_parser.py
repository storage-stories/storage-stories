#!/usr/bin/env python3
"""
Script to parse chat log files and extract messages from Jakob.
Format: [DD/MM/YYYY, HH:MM:SS] Username: Message
"""

import re
import json
from pathlib import Path

def extract_jakob_messages(file_path):
    """
    Extracts messages sent by Jakob from a chat log file.
    
    Args:
        file_path: Path to the chat log file
    
    Returns:
        List of dictionaries with timestamp, username, and message
    """
    jakob_messages = []
    
    # Pattern to match: [timestamp] Username: Message
    pattern = r'\[(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})\] ([^:]+): (.+)'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(pattern, line)
                if match:
                    timestamp, username, message = match.groups()
                    
                    # Filter for Jakob's messages
                    if username.strip() == 'Jakob':
                        jakob_messages.append({
                            'timestamp': timestamp,
                            'username': username,
                            'message': message
                        })
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return jakob_messages

def main():
    # Specify your input file here
    input_file = '_chat.txt'  # Change this to your file path
    
    messages = extract_jakob_messages(input_file)

    i_ = {}

    if messages:
        # Save results to JSON
        output_file = 'files_scan_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        
        print(f"Found {len(messages)} message(s) from Jakob")
        print(f"Results saved to '{output_file}'")
        
        # Also print to console
        print("\nJakob's messages:")
        for msg in messages:
            # print(f"[{msg['timestamp']}] {msg['message']}")
            
            # Check if message contains " I " (at beginning or middle)
            message = msg['message']
            # Look for " I " with word boundary, or "I " at the start
            # Captures words including apostrophes/quotes (e.g., "didn't", "I'm")
            match = re.search(r"\byou\s+([a-zA-Z'’]+)", message)
            if match:
                following_word = match.group(1)
                print(f"  → Found 'I' followed by: {following_word}")
                if following_word in i_:
                    i_[following_word] = i_[following_word] + 1
                else:
                    i_[following_word] = 1
    else:
        print("No messages from Jakob found.")

    print(i_)

if __name__ == '__main__':
    main()
