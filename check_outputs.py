import json

notebooks = [
    r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week1_eda\5_feature_engineering.ipynb",
    r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week1_eda\6_ridesharing_eda.ipynb",
    r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week2_synthetic_data\1_confounding_demo.ipynb",
    r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week2_synthetic_data\2_complex_data_generation.ipynb",
    r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week3_segmentation\1_user_segmentation.ipynb",
]

for path in notebooks:
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    total_cells = len(nb.get('cells', []))
    cells_with_output = sum(1 for c in nb['cells'] if c.get('cell_type') == 'code' and c.get('outputs'))
    code_cells = sum(1 for c in nb['cells'] if c.get('cell_type') == 'code')
    
    name = path.split('\\')[-1]
    print(f"{name}: {cells_with_output}/{code_cells} code cells have outputs")
