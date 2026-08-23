# Assembler for test_e2e_remediation_tiers.py
import os
import py_compile

e2e_dir = os.path.dirname(os.path.abspath(__file__))
parts = [
    'part0_header.py',
    'part1_tier1_a.py',
    'part2_tier1_b.py',
    'part3_tier2_a.py',
    'part4_tier2_b.py',
    'part5_tier3.py',
    'part6_tier4.py'
]

output_file = os.path.join(e2e_dir, 'test_e2e_remediation_tiers.py')

with open(output_file, 'w', encoding='utf-8') as out_f:
    for part in parts:
        part_path = os.path.join(e2e_dir, part)
        if os.path.exists(part_path):
            with open(part_path, 'r', encoding='utf-8') as in_f:
                out_f.write(in_f.read())
                out_f.write('\n\n')
        else:
            print(f'Warning: Part {part} does not exist at {part_path}')

print(f'Successfully assembled {output_file}')
py_compile.compile(output_file, doraise=True)
print('Compilation check passed with 0 syntax errors!')
