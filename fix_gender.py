import json
import os

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week2_synthetic_data\2_complex_data_generation.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if "is_urban = np.random.binomial(n=1, p=URBAN_RATIO, size=self.n)" in source and "gender" not in source:
            # Add gender generation
            source = source.replace(
                "age = np.clip(np.random.normal(AGE_MEAN, AGE_STD, self.n), 18, 60).astype(int)",
                "age = np.clip(np.random.normal(AGE_MEAN, AGE_STD, self.n), 18, 60).astype(int)\n        gender = np.random.choice(['Male', 'Female', 'Unknown'], size=self.n, p=[0.55, 0.40, 0.05])"
            )
            # Add gender to DataFrame
            source = source.replace(
                "'age': age,",
                "'age': age,\n            'gender': gender,"
            )
            
            lines = [line + '\n' for line in source.split('\n')]
            if lines:
                lines[-1] = lines[-1].rstrip('\n')
            cell['source'] = lines
            break

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
