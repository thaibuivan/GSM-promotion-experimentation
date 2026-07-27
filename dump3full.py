import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week3_segmentation\1_user_segmentation.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('notebook3_full.py', 'w', encoding='utf-8') as fout:
    for i, cell in enumerate(nb.get('cells', [])):
        fout.write(f"\n# === CELL {i} ({cell['cell_type']}) ===\n")
        fout.write(''.join(cell.get('source', [])) + '\n')
