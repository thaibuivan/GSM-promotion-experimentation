import json
import sys

filepath = r'D:\Intern VSF\GSM-promotion-experimentation\notebooks\week4_ab_testing\1_ab_test_analysis.ipynb'
with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        changed = False
        for line in source:
            if "if 'Persona A' in df['persona'].values:" in line:
                changed = True
                continue
            if "df['persona'] = df['cluster_id'].map(persona_names)" in line:
                changed = True
                continue
            if "# Không cần map nữa vì data Phase 2 đã có sẵn tên persona chuẩn!" in line:
                changed = True
                continue
            if "target_persona = 'Airport Business'" in line:
                new_source.append("target_persona = 'Urban Regulars'  # Chọn nhóm mục tiêu có ATE dương\n")
                changed = True
                continue
            new_source.append(line)
        if changed:
            cell['source'] = new_source

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Week 4 Notebook patched successfully.")
