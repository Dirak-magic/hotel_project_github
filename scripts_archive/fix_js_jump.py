import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the old normalizer JS with the robust one
old_js = '''    // Normalize slide heights to prevent jumping
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
    }'''

new_js = '''    // Normalize slide heights to prevent jumping (Robust for hidden items)
    function normalizeSlideHeights() {
        let items = document.querySelectorAll('#saleCarousel .carousel-item .sale-section');
        let maxHeight = 0;
        
        // Reset and measure
        items.forEach(function(item) {
            item.style.height = 'auto';
            let parent = item.closest('.carousel-item');
            
            // Bootstrap hides non-active items with display:none, making height 0.
            // We temporarily show them off-screen to measure their true height.
            let wasHidden = false;
            if (window.getComputedStyle(parent).display === 'none') {
                wasHidden = true;
                parent.style.display = 'block';
                parent.style.visibility = 'hidden';
                parent.style.position = 'absolute';
            }
            
            let h = item.offsetHeight;
            if (h > maxHeight) {
                maxHeight = h;
            }
            
            // Restore hidden state
            if (wasHidden) {
                parent.style.display = '';
                parent.style.visibility = '';
                parent.style.position = '';
            }
        });
        
        // Apply tallest height to all
        items.forEach(function(item) {
            item.style.height = maxHeight + 'px';
        });
    }'''

if old_js in text:
    text = text.replace(old_js, new_js)
    with open('templates/home.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced JS normalizer")
else:
    print("Old JS not found. Searching with regex...")
    pattern = r'// Normalize slide heights to prevent jumping.*?item\.style\.height = maxHeight \+ \'px\';\n        \}\);\n    \}'
    text = re.sub(pattern, new_js, text, flags=re.DOTALL)
    with open('templates/home.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced with regex.")
