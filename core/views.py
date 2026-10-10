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

    from .models import SiteSetting
    site_setting = SiteSetting.objects.first()
    if site_setting and site_setting.disable_availability_check:
        return JsonResponse({'error': 'Hệ thống tra cứu lịch trống đang được bảo trì. Vui lòng thử lại sau hoặc liên hệ Hotline để đặt phòng.'}, status=503)

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
            
            all_ws = spreadsheet.worksheets()
            tabs_to_process = []
            
            import re
            
            # Helper function to extract month and year from tab title
            def extract_tab_month_year(title, current_year):
                title = title.lower().strip()
                # Find explicit year (e.g. 2024, 2025, 2026)
                m_year_4 = re.search(r'\b(202[4-9]|20[3-9]\d)\b', title)
                year = int(m_year_4.group(1)) if m_year_4 else None
                
                # Find explicit month (e.g. t10, tháng 10, 10/2024)
                m_month = re.search(r'(?:t|tháng|thang|thg)\s*(0?[1-9]|1[0-2])(?!\d)', title)
                if m_month:
                    month = int(m_month.group(1))
                else:
                    m_month_year = re.search(r'\b(0?[1-9]|1[0-2])\s*[/.-]\s*(20\d\d|\d\d)\b', title)
                    if m_month_year:
                        month = int(m_month_year.group(1))
                        y_str = m_month_year.group(2)
                        if not year:
                            year = int(y_str) if len(y_str) == 4 else 2000 + int(y_str)
                    else:
                        m_num = re.fullmatch(r'(0?[1-9]|1[0-2])', title)
                        if m_num:
                            month = int(m_num.group(1))
                        else:
                            return None, None
                            
                if not year:
                    year = current_year
                return month, year

            for ws in all_ws:
                m, y = extract_tab_month_year(ws.title, now.year)
                if m and y:
                    # Only process current and future months, or up to 1 month in the past (to support current week)
                    tab_date = datetime.date(y, m, 1)
                    current_date = datetime.date(now.year, now.month, 1)
                    diff_months = (tab_date.year - current_date.year) * 12 + tab_date.month - current_date.month
                    
                    if -1 <= diff_months <= 24: # Get up to 2 years ahead
                        tabs_to_process.append({'ws': ws, 'month': m, 'year': y, 'is_fallback': False})
            
            # Sort tabs chronologically
            tabs_to_process.sort(key=lambda x: (x['year'], x['month']))
            
            if not tabs_to_process:
                # Fallback to first few tabs if no matches found
                for ws in all_ws[:6]:
                    tabs_to_process.append({'ws': ws, 'month': now.month, 'year': now.year, 'is_fallback': True})
                    
            # Limit to at most 18 tabs to prevent Google API timeout
            tabs_to_process = tabs_to_process[:18]
                
            meta = spreadsheet.fetch_sheet_metadata()
            
            prop_data = {'meta': meta, 'tabs': []}
            for tab_info in tabs_to_process:
                sheet = tab_info['ws']
                data = sheet.get_all_values()
                if data:
                    prop_data['tabs'].append({
                        'title': sheet.title,
                        'month': tab_info['month'],
                        'year': tab_info['year'],
                        'is_fallback': tab_info['is_fallback'],
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
            tab_month = tab.get('month', now.month)
            tab_year = tab.get('year', now.year)
            
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
            month_map = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
            
            import re as regex
            for r_idx, row in enumerate(data[:10]):
                dates_found = 0
                temp_date_cols = {}
                
                prev_month = tab_month
                prev_year = tab_year
                
                for c_idx, cell in enumerate(row):
                    cell_str = str(cell).strip().lower()
                    if not cell_str: continue
                    
                    m1 = regex.match(r'^(\d{1,2})[-/](\d{1,2})', cell_str)
                    m2 = regex.match(r'^(\d{1,2})[-/]([a-z]{3})', cell_str)
                    m3 = regex.fullmatch(r'^\d{1,2}$', cell_str)
                    
                    day = None
                    month = None
                    year = tab_year
                    
                    if m1:
                        # DD/MM or MM/DD. Assume DD/MM for Vietnam usually, unless DD > 12.
                        g1, g2 = int(m1.group(1)), int(m1.group(2))
                        if g2 > 12: 
                            day, month = g2, g1 # MM/DD
                        else: 
                            day, month = g1, g2 # DD/MM default
                    elif m2:
                        day = int(m2.group(1))
                        month_str = m2.group(2)
                        month = month_map.get(month_str, tab_month)
                    elif m3:
                        day = int(cell_str)
                        month = tab_month
                        
                    if day and month and 1 <= day <= 31 and 1 <= month <= 12:
                        # Handle year transition (e.g. Dec to Jan in the same tab, or Nov to Dec where tab_month is Jan)
                        # We use a simple heuristic based on tab_month
                        if month == 12 and tab_month == 1:
                            year = tab_year - 1
                        elif month == 1 and tab_month == 12:
                            year = tab_year + 1
                            
                        # If just using m3 (only numbers 1-31), handle transition from 31 to 1
                        if m3 and day < 15 and prev_month:
                            # if day drops significantly (e.g. 31 -> 1), increment month
                            if dates_found > 0 and day < 15:
                                # We need to know previous day to be sure, but we can just rely on tab_month for m3.
                                # Let's try to get previous day string.
                                # Actually, it's safer to just use tab_month unless we explicitly see a wrap.
                                pass
                                
                        dates_found += 1
                        prev_month = month
                        prev_year = year
                        
                        try:
                            # Validate date by creating datetime object
                            valid_date = datetime.date(year, month, day)
                            formatted = valid_date.strftime('%Y-%m-%d')
                            temp_date_cols[c_idx] = formatted
                        except ValueError:
                            pass # Invalid date like 30/02
                        
                if dates_found >= 15 or len(temp_date_cols) >= 5:
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
        # Thay vì hiện lỗi kỹ thuật hoặc cấu trúc thư mục rỗng, hiện thông báo bảo trì
        return JsonResponse({'error': 'Hệ thống tra cứu đang tạm thời gián đoạn hoặc bảo trì. Vui lòng liên hệ trực tiếp qua Hotline để kiểm tra phòng trống.'}, status=503)

def contact_view(request):
    from .models import Property, Brand
    properties = Property.objects.select_related('brand').all()
    all_brands = Brand.objects.all()
    return render(request, 'contact.html', {'properties': properties, 'all_brands': all_brands})
