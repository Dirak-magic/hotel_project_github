import os
import django
import gspread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Property

properties = Property.objects.all()
for prop in properties:
    print(f"\n=== Property: {prop.name} ===")
    if not prop.google_sheet_id:
        print("No sheet ID")
        continue
    
    creds_path = prop.google_sheet_credentials.path if prop.google_sheet_credentials else None
    if not creds_path or not os.path.exists(creds_path):
        print("No creds")
        continue
        
    try:
        client = gspread.service_account(filename=creds_path)
        spreadsheet = client.open_by_key(prop.google_sheet_id)
        
        for ws in spreadsheet.worksheets()[:5]:
            print(f"  Tab: '{ws.title}'")
            # Print the first row that looks like it has dates
            data = ws.get_all_values()[:10]
            date_row = None
            for row in data:
                # check if row has things like '1/11'
                import re
                dates = [c for c in row if re.match(r'^\d{1,2}[-/]\d{1,2}', str(c).strip())]
                if len(dates) > 5:
                    date_row = row
                    break
            
            if date_row:
                print(f"    Date row format sample: {date_row[1:5]} ...")
            else:
                print(f"    No date row found! First 2 rows:")
                for r in data[:2]:
                    print(f"      {r[:10]}")
    except Exception as e:
        print(f"Error: {e}")
