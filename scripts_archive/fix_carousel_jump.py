import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Simplify the inline height style on sale-section
pattern = r'; height: 100%; min-height: 800px;'
text = re.sub(pattern, '; min-height: 700px;', text)

# 2. Add the normalizer JS
js_normalizer = '''
    // Normalize slide heights to prevent jumping
    function normalizeSlideHeights() {
        let items = document.querySelectorAll('#saleCarousel .carousel-item .sale-section');
        let maxHeight = 0;
        
        // Reset all heights to auto to measure natural height
        items.forEach(function(item) {
            item.style.height = 'auto';
        });
        
        // Find the tallest
        items.forEach(function(item) {
            if (item.offsetHeight > maxHeight) {
                maxHeight = item.offsetHeight;
            }
        });
        
        // Apply tallest height to all
        items.forEach(function(item) {
            item.style.height = maxHeight + 'px';
        });
    }
    
    window.addEventListener('load', normalizeSlideHeights);
    window.addEventListener('resize', normalizeSlideHeights);
'''

# Find a script tag to insert it into
text = text.replace('// Force start the carousel', js_normalizer + '\n    // Force start the carousel')

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(text)
