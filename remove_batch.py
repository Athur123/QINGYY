#!/usr/bin/env python3
"""Remove batch calculation code from calculator HTML file"""

import re

# Read the file
with open('prototype/qingyang-calculator-redesigned.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove batch section CSS (from "/* Batch Section Styles */" to before "/* Compare Section */")
pattern1 = r'/\*\s*Batch Section Styles.*?End Batch Section.*?\*/'
content = re.sub(pattern1, '', content, flags=re.DOTALL)

# Remove batch-section from print media query
content = re.sub(r'\.batch-section,\s*', '', content)

# Remove batch section HTML (from "<!-- Batch Section -->" to "</section>" after batch)
pattern2 = r'<!--\s*Batch Section.*?<!--\s*End Batch Section.*?-->'
content = re.sub(pattern2, '', content, flags=re.DOTALL)

# Remove batch calculation button from page actions
pattern3 = r'<button[^>]*onclick="toggleBatchSection\(\)"[^>]*>.*?</button>\s*'
content = re.sub(pattern3, '', content, flags=re.DOTALL)

# Remove batch-related variable
content = re.sub(r"let batchResults = \[\];\s*", '', content)

# Remove batch JavaScript functions
batch_functions = [
    'toggleBatchSection',
    'setBatchPresets',
    'calculateBatch',
    'renderBatchResults',
    'clearBatch',
    'exportBatchToCSV'
]

for func in batch_functions:
    # Match function declaration and its body
    pattern = rf"\/\*\*\s*\n\s*\*\s*{func.replace('toggle', 'Toggle').replace('set', 'Set').replace('calculate', 'Calculate').replace('render', 'Render').replace('clear', 'Clear').replace('export', 'Export')}.*?function {func}\(\)[^{{]*{{.*?^\s*}}\s*"
    content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)

# Clean up any double newlines
content = re.sub(r'\n{3,}', '\n\n', content)

# Write back
with open('prototype/qingyang-calculator-redesigned.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Batch calculation code removed successfully!")
