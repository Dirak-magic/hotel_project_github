from django.shortcuts import render, get_object_or_404
from .models import Brand, RoomCategory
import json
import gspread
from django.http import JsonResponse
from django.core.cache import cache
import datetime
from django_ratelimit.decorators import ratelimit

def home(request):
    brands = Brand.objects.all()
    sale_properties = Brand.objects.filter(sale_active=True)
    return render(request, 'home.html', {'brands': brands, 'sale_properties': sale_properties})

def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    # Tối ưu truy vấn: Kéo luôn các cơ sở và hạng phòng ra
    properties = brand.properties.prefetch_related('room_categories').all()
    all_brands = Brand.objects.all()
    return render(request, 'brand_detail.html', {'brand': brand, 'properties': properties, 'all_brands': all_brands})

def room_detail(request, pk):
    room = get_object_or_404(RoomCategory, pk=pk)
    all_brands = Brand.objects.all()
    return render(request, 'room_detail.html', {'room': room, 'prop': room.property, 'all_brands': all_brands})

@ratelimit(key='ip', rate='20/m', block=False)
def check_availability(request, pk):
    if getattr(request, 'limited', False):
        return JsonResponse({'error': 'Bạn đã tra cứu quá nhiều lần. Vui lòng thử lại sau 1 phút.'}, status=429)

    room = get_object_or_404(RoomCategory, pk=pk)
    prop = room.property
    
    if not prop.google_sheet_credentials or not prop.google_sheet_id or not room.sheet_row_name:
        return JsonResponse({'error': 'Chưa cấu hình Google Sheet cho cơ sở hoặc hạng phòng này.'}, status=400)

    # Cache level 1: Room Specific Data (Super fast)
    room_cache_key = f'room_avail_{room.id}'
    cached_room_data = cache.get(room_cache_key)
    if cached_room_data is not None:
        return JsonResponse(cached_room_data)

    try:
        # Cache level 2: Property Level Raw Data (Fast, avoids Google API)
        prop_cache_key = f'prop_sheet_data_{prop.google_sheet_id}'
        prop_data = cache.get(prop_cache_key)
        
        now = datetime.datetime.now()
        
        if not prop_data:
            import os
            # Auth using gspread directly
            creds_path = None
            if prop.google_sheet_credentials and os.path.exists(prop.google_sheet_credentials.path):
                creds_path = prop.google_sheet_credentials.path
            else:
                from .models import Property
                for other_prop in Property.objects.filter(google_sheet_id=prop.google_sheet_id):
                    if other_prop.google_sheet_credentials and os.path.exists(other_prop.google_sheet_credentials.path):
                        creds_path = other_prop.google_sheet_credentials.path
                        break
            
            if not creds_path:
                return JsonResponse({'error': 'Không tìm thấy file credentials hợp lệ cho Sheet ID này.'}, status=400)

            client = gspread.service_account(filename=creds_path)
            spreadsheet = client.open_by_key(prop.google_sheet_id)
            
            # Find tabs for Current Month and Next Month
            current_tab = f"T{now.month}/{now.year}"
            next_month = now.month + 1 if now.month < 12 else 1
            next_year = now.year if now.month < 12 else now.year + 1
            next_tab = f"T{next_month}/{next_year}"
            
            all_ws = spreadsheet.worksheets()
            # Loại bỏ toàn bộ khoảng trắng để so sánh tên tab (tránh lỗi do gõ dư dấu cách ở giữa hoặc 2 đầu)
            ws_dict = {ws.title.replace(' ', '').lower(): ws for ws in all_ws}
            
            tabs_to_process = []
            if current_tab.lower() in ws_dict:
                tabs_to_process.append(ws_dict[current_tab.lower()])
            if next_tab.lower() in ws_dict:
                tabs_to_process.append(ws_dict[next_tab.lower()])
                
            if not tabs_to_process:
                tabs_to_process = [spreadsheet.sheet1] # Fallback
                
            meta = spreadsheet.fetch_sheet_metadata()
            
            prop_data = {'meta': meta, 'tabs': []}
            for sheet in tabs_to_process:
                data = sheet.get_all_values()
                if data:
                    prop_data['tabs'].append({
                        'title': sheet.title,
                        'data': data
                    })
                    
            # Cache property raw data for 10 minutes
            cache.set(prop_cache_key, prop_data, 600)
            
        # Process the raw data for the specific room
        booked_dates = []
        availability = {}
        
        is_composite = '+' in room.sheet_row_name
        separator = '+' if is_composite else ','
        target_room_names = [n.strip().lower() for n in room.sheet_row_name.split(separator) if n.strip()]
        total_rooms = len(target_room_names)
        
        if not target_room_names:
            return JsonResponse({'error': 'Tên phòng trống. Vui lòng cấu hình Tên phòng.'}, status=400)

        for tab in prop_data['tabs']:
            sheet_title = tab['title']
            data = tab['data']
            
            merged_cells = []
            for s in prop_data['meta'].get('sheets', []):
                if s.get('properties', {}).get('title') == sheet_title:
                    merged_cells = s.get('merges', [])
                    break
                    
            for m in merged_cells:
                start_row = m.get('startRowIndex', 0)
                end_row = m.get('endRowIndex', 0)
                start_col = m.get('startColumnIndex', 0)
                end_col = m.get('endColumnIndex', 0)
                
                try:
                    val = data[start_row][start_col]
                except IndexError:
                    val = "booked"
                    
                for r in range(start_row, end_row):
                    while len(data) <= r:
                        data.append([])
                    for c in range(start_col, end_col):
                        while len(data[r]) <= c:
                            data[r].append("")
                        data[r][c] = val

            date_row_idx = -1
            date_cols = {}
            current_year = now.year
            month_map = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
            
            import re as regex
            for r_idx, row in enumerate(data[:10]):
                dates_found = 0
                temp_date_cols = {}
                for c_idx, cell in enumerate(row):
                    cell_str = str(cell).strip().lower()
                    if not cell_str: continue
                    
                    m1 = regex.match(r'^(\d{1,2})[-/](\d{1,2})', cell_str)
                    m2 = regex.match(r'^(\d{1,2})[-/]([a-z]{3})', cell_str)
                    
                    day = None
                    month = None
                    if m1:
                        day, month = m1.groups()
                    elif m2:
                        day, month_str = m2.groups()
                        month = month_map.get(month_str, None)
                        
                    if day and month:
                        dates_found += 1
                        # Lấy năm từ tên tab (nếu có), nếu không lấy năm hiện tại
                        year_to_use = current_year
                        try:
                            if '20' in sheet_title:
                                year_to_use = int(sheet_title.split('/')[-1])
                        except:
                            pass
                            
                        formatted = f"{year_to_use}-{str(month).zfill(2)}-{str(day).zfill(2)}"
                        temp_date_cols[c_idx] = formatted
                        
                if dates_found >= 3:
                    date_row_idx = r_idx
                    date_cols = temp_date_cols
                    break
                    
            if date_row_idx == -1:
                continue # Bỏ qua tab này nếu không tìm thấy ngày
                
            matched_room_rows = []
            for r_idx, row in enumerate(data):
                if not row: continue
                # Thường tên phòng nằm ở cột A hoặc B
                cell_vals = [str(c).strip().lower() for c in row[:2]]
                is_matched = False
                for target_name in target_room_names:
                    for cell_val in cell_vals:
                        # Dùng substring: Nếu tên cài trong Admin (VD: 'R01') có chứa trong file Sheet (VD: 'SUN POOL SUITE (R01)')
                        if target_name and target_name in cell_val:
                            matched_room_rows.append(row)
                            is_matched = True
                            break
                    if is_matched:
                        break
                        
            if not matched_room_rows:
                continue

            for c_idx, date_str in date_cols.items():
                if is_composite:
                    is_booked = False
                    for row in matched_room_rows:
                        cell_val = str(row[c_idx]).strip() if c_idx < len(row) else ""
                        if cell_val:
                            is_booked = True
                            break
                    avail_count = 0 if is_booked else 1
                    availability[date_str] = {'available': avail_count, 'total': 1}
                    if is_booked:
                        booked_dates.append(date_str)
                else:
                    booked_count = 0
                    for row in matched_room_rows:
                        cell_val = str(row[c_idx]).strip() if c_idx < len(row) else ""
                        if cell_val: 
                            booked_count += 1
                    
                    avail_count = total_rooms - booked_count
                    if avail_count < 0: avail_count = 0
                    
                    availability[date_str] = {'available': avail_count, 'total': total_rooms}
                    if avail_count == 0:
                        booked_dates.append(date_str)
                        
        response_data = {'booked_dates': list(set(booked_dates)), 'availability': availability}
        # Cache room specific result for 10 minutes
        cache.set(room_cache_key, response_data, 600)
        
        return JsonResponse(response_data)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

def contact_view(request):
    from .models import Property, Brand
    properties = Property.objects.select_related('brand').all()
    all_brands = Brand.objects.all()
    return render(request, 'contact.html', {'properties': properties, 'all_brands': all_brands})
