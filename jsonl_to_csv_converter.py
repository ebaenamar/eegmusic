#!/usr/bin/env python3
"""
JSONL to CSV Converter for Neurable EEG Data
Converts JSONL format to CSV format compatible with neurable_adapter
"""

import json
import csv
import sys
from pathlib import Path

def convert_jsonl_to_csv(jsonl_path: str, csv_path: str = None):
    """
    Convert JSONL file to CSV format.
    
    Args:
        jsonl_path: Path to input JSONL file
        csv_path: Path to output CSV file (optional, auto-generated if not provided)
    """
    jsonl_file = Path(jsonl_path)
    
    if not jsonl_file.exists():
        print(f"❌ Error: File not found: {jsonl_path}")
        return False
    
    # Auto-generate CSV path if not provided
    if csv_path is None:
        csv_path = jsonl_file.with_suffix('.csv')
    
    csv_file = Path(csv_path)
    
    print(f"📂 Reading: {jsonl_file}")
    print(f"💾 Writing: {csv_file}")
    
    try:
        # Read first line to get column names
        with open(jsonl_file, 'r') as f:
            first_line = f.readline()
            if not first_line:
                print("❌ Error: Empty file")
                return False
            
            first_record = json.loads(first_line)
            columns = list(first_record.keys())
        
        # Write CSV
        rows_written = 0
        with open(jsonl_file, 'r') as f_in, open(csv_file, 'w', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=columns)
            writer.writeheader()
            
            for line_num, line in enumerate(f_in, 1):
                try:
                    record = json.loads(line.strip())
                    writer.writerow(record)
                    rows_written += 1
                except json.JSONDecodeError as e:
                    print(f"⚠️ Warning: Skipping line {line_num}: {e}")
                    continue
        
        print(f"✅ Success! Converted {rows_written} rows")
        print(f"📊 Columns: {len(columns)}")
        print(f"   {', '.join(columns[:5])}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python jsonl_to_csv_converter.py <input.jsonl> [output.csv]")
        print("\nExample:")
        print("  python jsonl_to_csv_converter.py /Users/e.baena/Desktop/eeg_stream.jsonl")
        print("  python jsonl_to_csv_converter.py input.jsonl output.csv")
        sys.exit(1)
    
    jsonl_path = sys.argv[1]
    csv_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 60)
    print("🔄 JSONL to CSV Converter - Neurable EEG Data")
    print("=" * 60)
    print()
    
    success = convert_jsonl_to_csv(jsonl_path, csv_path)
    
    if success:
        print("\n✅ Conversion complete!")
        if csv_path is None:
            csv_path = Path(jsonl_path).with_suffix('.csv')
        print(f"\n🎵 Ready to use with:")
        print(f"   python neurable_music_generator.py {csv_path}")
    else:
        print("\n❌ Conversion failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
