import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week3_segmentation\1_user_segmentation.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if "persona_names = {" in source and "Suburban Commuters" in source:
            # Delete this cell's content entirely except the save command
            if "df.to_csv" in source:
                new_source = """# Lưu lại bộ dữ liệu có chứa nhãn Persona để dùng cho các tuần sau
df.to_csv('../../data/processed/segmented_simulation_data.csv', index=False)
print('Đã lưu file segmented_simulation_data.csv thành công với các Persona V2 mới!')"""
                
                lines = [line + '\n' for line in new_source.split('\n')]
                if lines:
                    lines[-1] = lines[-1].rstrip('\n')
                cell['source'] = lines
            break

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
