import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = {
    "AB Test (Tuan 4)": r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week4_ab_testing\1_ab_test_analysis.ipynb",
    "AA Test (Tuan 5)": r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week5_aa_testing\1_aa_test_pipeline.ipynb",
}

for name, path in files.items():
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    all_code = ""
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            all_code += ''.join(cell['source']) + '\n'
    
    with open(f'check_{name[:2]}.txt', 'w', encoding='utf-8') as out:
        out.write(f"FILE: {name}\n{'='*60}\n")
        lines = all_code.split('\n')
        for line in lines:
            if any(kw in line for kw in ['persona', 'target_persona', 'personas_to_test', 'n_clusters', 'Airport', 'Urban', 'Suburban', 'Cash']):
                out.write(line.strip() + '\n')

print("Done - check check_AB.txt and check_AA.txt")
