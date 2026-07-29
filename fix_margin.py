import json

with open('notebooks/week4_ab_testing/1_ab_test_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if 'margin_per_trip = 10.0' in line:
                source[i] = line.replace('10.0', '20.0').replace('10 USD', '20 USD').replace('10,000 VND', '20,000 VND')

with open('notebooks/week4_ab_testing/1_ab_test_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
