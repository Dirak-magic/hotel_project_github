import re

with open('templates/brand_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the block to replace:
# From <div class="container-fluid position-relative overflow-hidden p-0" style="background-color: var(--bs-body-bg);">
# To the end of the <div class="row w-100 m-0 align-items-center"> ... </div>
# Which ends at the closing </div> before <style>
