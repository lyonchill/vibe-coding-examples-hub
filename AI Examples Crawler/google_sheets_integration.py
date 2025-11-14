"""
Google Sheets Integration
Automatically add approved examples to Google Sheets
"""

import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googlespreadsheet import Spreadsheet

# If you want to use Google Sheets, you'll need:
# 1. Create a service account in Google Cloud Console
# 2. Download the credentials JSON file
# 3. Share your Google Sheet with the service account email
# 4. Install: pip install gspread google-auth

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'google-credentials.json'  # Your service account key file
SPREADSHEET_ID = os.getenv('GOOGLE_SHEET_ID', 'YOUR_SHEET_ID_HERE')


def setup_google_sheets():
    """Initialize Google Sheets connection"""
    try:
        import gspread
        
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.sheet1  # Use first worksheet
        
        return worksheet
    except Exception as e:
        print(f"Error setting up Google Sheets: {e}")
        return None


def add_example_to_sheet(worksheet, example: dict):
    """Add a single example to Google Sheets"""
    try:
        row = [
            example['title'],
            example['description'],
            ', '.join(example['ai_tools_used']),
            ', '.join(example['category_tags']),
            example['source_platform'],
            example['original_url'],
            example['creator_name'],
            example['creator_link'],
            example['thumbnail_url'],
            example['date_added'],
            example.get('relevance_score', ''),
            example.get('build_complexity', '')
        ]
        
        worksheet.append_row(row)
        print(f"✅ Added to sheet: {example['title']}")
        return True
        
    except Exception as e:
        print(f"❌ Error adding to sheet: {e}")
        return False


def batch_add_examples(json_file: str):
    """Add all examples from JSON file to Google Sheets"""
    
    print("📊 Connecting to Google Sheets...")
    worksheet = setup_google_sheets()
    
    if not worksheet:
        print("❌ Failed to connect to Google Sheets")
        return
    
    # Check if headers exist, if not add them
    try:
        headers = worksheet.row_values(1)
        if not headers:
            worksheet.append_row([
                'Title', 'Description', 'AI Tools Used', 'Category Tags',
                'Source Platform', 'Original URL', 'Creator Name', 
                'Creator Link', 'Thumbnail URL', 'Date Added',
                'Relevance Score', 'Build Complexity'
            ])
            print("Added headers to sheet")
    except:
        pass
    
    # Load examples from JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    
    print(f"Found {len(examples)} examples to add")
    
    # Add each example
    success_count = 0
    for example in examples:
        if add_example_to_sheet(worksheet, example):
            success_count += 1
    
    print(f"\n✅ Successfully added {success_count}/{len(examples)} examples to Google Sheets")


def create_setup_instructions():
    """Print setup instructions"""
    print("""
    📋 Google Sheets Setup Instructions:
    
    1. Go to Google Cloud Console (console.cloud.google.com)
    2. Create a new project or select existing
    3. Enable Google Sheets API
    4. Create Service Account:
       - IAM & Admin → Service Accounts → Create Service Account
       - Grant it the 'Editor' role
       - Create Key → JSON → Download
    5. Save the JSON file as 'google-credentials.json' in this folder
    6. Create a Google Sheet for your data
    7. Share the sheet with the service account email (in the JSON file)
    8. Copy the sheet ID from URL:
       https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
    9. Set GOOGLE_SHEET_ID in your .env file
    10. Install required package:
        pip install gspread google-auth
    
    Then run: python google_sheets_integration.py [json_file]
    """)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python google_sheets_integration.py <json_file>")
        print("\nExample: python google_sheets_integration.py found_examples_20241112.json")
        print("\nOr run: python google_sheets_integration.py --setup")
        print("to see setup instructions")
        
        if '--setup' in sys.argv:
            create_setup_instructions()
        
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        sys.exit(1)
    
    if not os.path.exists(CREDENTIALS_FILE):
        print("❌ Google credentials file not found!")
        print("\nRun with --setup flag to see instructions:")
        print("python google_sheets_integration.py --setup")
        sys.exit(1)
    
    batch_add_examples(json_file)
