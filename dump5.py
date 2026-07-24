import json

with open('notebooks/week5_aa_testing/1_aa_test_pipeline.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('notebook5_dump.py', 'w', encoding='utf-8') as fout:
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'code':
            fout.write(''.join(cell['source']) + '\n\n')
