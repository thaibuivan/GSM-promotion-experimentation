import json

with open('notebooks/week4_ab_testing/1_ab_test_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('notebook4_dump.py', 'w', encoding='utf-8') as fout:
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'code':
            fout.write(''.join(cell['source']) + '\n\n')
