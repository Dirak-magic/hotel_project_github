import re

def replace_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # In brand_detail, the tabs were "Các Cơ sở" -> "Các Chi nhánh"
    text = text.replace('Nav Tabs cho Các Cơ sở', 'Nav Tabs cho Các Chi nhánh')
    text = text.replace('Cơ sở {{ prop.name }}', 'Chi nhánh {{ prop.name }}')
    text = text.replace('Đang cập nhật cơ sở', 'Đang cập nhật chi nhánh')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

replace_text('templates/brand_detail.html')
print('Updated brand_detail.html text')
