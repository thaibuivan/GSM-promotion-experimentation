import json
import glob

notebooks = glob.glob('notebooks/**/*.ipynb', recursive=True)
has_error = False

for nb_path in sorted(notebooks):
    with open(nb_path, 'r', encoding='utf-8') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            print(f'❌ Lỗi parse JSON file: {nb_path}')
            continue
            
    print(f'\n--- Kiểm tra {nb_path} ---')
    cells = nb.get('cells', [])
    output_count = 0
    error_count = 0
    
    for i, cell in enumerate(cells):
        if cell['cell_type'] == 'code':
            outputs = cell.get('outputs', [])
            if outputs:
                output_count += 1
            for out in outputs:
                if out.get('output_type') == 'error':
                    ename = out.get("ename", "Unknown")
                    evalue = out.get("evalue", "Unknown")
                    print(f'❌ Lỗi thực thi ở Cell {i}: {ename} - {evalue}')
                    error_count += 1
                    has_error = True
                    
    print(f'Tổng số Cell có Output: {output_count}')
    if error_count == 0:
        print('✅ Không có lỗi Runtime.')
