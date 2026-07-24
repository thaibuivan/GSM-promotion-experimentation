import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week3_segmentation\1_user_segmentation.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if "colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']" in source:
            # Fix colors and title
            source = source.replace(
                "colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']",
                "colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']"
            )
            source = source.replace(
                "Radar Chart của 4 Personas",
                "Radar Chart của 5 Personas"
            )
            
            lines = [line + '\n' for line in source.split('\n')]
            if lines:
                lines[-1] = lines[-1].rstrip('\n')
            cell['source'] = lines
            break

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
