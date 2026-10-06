import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove margin-top: -100px
text = text.replace('margin-top: -100px;', 'margin-top: 0;')

# 2. Change bottom: 120px to bottom: 20px
text = text.replace('bottom: 120px;', 'bottom: 20px;')

# 3. Increase min-height slightly to 850px to ensure it fits mobile text + timer, 
# and keep height: auto or height: 85vh. Wait, let's change to min-height: 850px; height: auto;
# Actually, height: 85vh works on mobile but some phones have small vh. Let's change it to min-height: 850px;
pattern = r'height: 85vh; min-height: 750px;'
text = re.sub(pattern, 'height: 100%; min-height: 800px;', text)

# Also let's make sure the text is not squeezed too much by reducing line-height on mobile
# Just leave line-height as is.

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed overlap')
