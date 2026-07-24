import json

with open('notebooks/week3_segmentation/1_user_segmentation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('notebook3_dump.py', 'w', encoding='utf-8') as fout:
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'code':
            fout.write(''.join(cell['source']) + '\n\n')
