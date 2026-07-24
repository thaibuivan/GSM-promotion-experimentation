import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week2_synthetic_data\2_complex_data_generation.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if "'age': age," in source and "customer_segment" not in source:
            # Add customer_segment generation
            source = source.replace(
                "'gender': gender,",
                "'gender': gender,\n            'customer_segment': np.random.choice(['Regular', 'Occasional', 'New'], size=self.n, p=[0.4, 0.4, 0.2]),"
            )
            
            lines = [line + '\n' for line in source.split('\n')]
            if lines:
                lines[-1] = lines[-1].rstrip('\n')
            cell['source'] = lines
            break

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
