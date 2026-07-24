import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week4_ab_testing\1_ab_test_analysis.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        
        # 1. Update hardcoded persona mapping for safety
        if "persona_names = {0:" in source:
            source = source.replace(
                "persona_names = {0: 'Suburban Commuters', 1: 'Urban Commuters', 2: 'Urban Leisure', 3: 'Suburban Occasionals'}",
                "# Không cần map nữa vì data Phase 2 đã có sẵn tên persona chuẩn!"
            )
            
        # 2. Update target persona for the first analysis
        if "target_persona = 'Suburban Commuters'" in source:
            source = source.replace(
                "target_persona = 'Suburban Commuters'",
                "target_persona = 'Airport Business' # THỬ NGHIỆM TRÊN NHÓM KHÁNG SALE"
            )
            
        # 3. Update the loop testing multiple personas
        if "personas_to_test = ['Suburban Commuters', 'Urban Leisure']" in source:
            source = source.replace(
                "personas_to_test = ['Suburban Commuters', 'Urban Leisure']",
                "personas_to_test = ['Airport Business', 'Cash Traditional', 'Urban Weekend Party', 'Urban Regulars', 'Suburban Occasionals']"
            )

        lines = [line + '\n' for line in source.split('\n')]
        if lines:
            lines[-1] = lines[-1].rstrip('\n')
        cell['source'] = lines

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
