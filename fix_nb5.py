import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week5_aa_testing\1_aa_test_pipeline.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if "target_persona = 'Suburban Commuters'" in source:
            # Replace target_persona with one that exists in V2
            source = source.replace(
                "target_persona = 'Suburban Commuters'",
                "target_persona = 'Urban Regulars'"
            )
            
            lines = [line + '\n' for line in source.split('\n')]
            if lines:
                lines[-1] = lines[-1].rstrip('\n')
            cell['source'] = lines
            break

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
