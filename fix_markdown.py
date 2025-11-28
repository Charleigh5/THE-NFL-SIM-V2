import re

file_path = r'c:\Users\cweir\.gemini\antigravity\brain\13f4fe55-cf7c-4f8b-8985-2e5541d3c0e1\implementation_plan.md'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace any list marker (number followed by dot and 2+ spaces) with single space
    new_content = re.sub(r'^(\d+\.)\s{2,}', r'\1 ', content, flags=re.MULTILINE)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully updated all list markers in the file.")
    print("Fixed all MD030 linting errors (list marker spacing).")
except Exception as e:
    print(f"Error: {e}")
