import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week2_synthetic_data\2_complex_data_generation.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = "".join(cell.get('source', []))
        if "'fare_rand': fare_rand" in source and "fare_obs" not in source:
            
            # Inject obs variables generation
            source = source.replace(
                "fare = y_rand * (5.0 * avg_distance + np.random.normal(0, 2.5, self.n))\n        fare_rand = np.clip(fare, 0, None).round(2)",
                """fare = y_rand * (5.0 * avg_distance + np.random.normal(0, 2.5, self.n))
        fare_rand = np.clip(fare, 0, None).round(2)
        
        prob_voucher = np.where(is_urban_leisure, 0.8, 0.2)
        treatment_obs = np.random.binomial(1, p=prob_voucher, size=self.n)
        y_obs = np.where(treatment_obs == 1, y1_rides, y0_rides)
        fare_obs = y_obs * (5.0 * avg_distance + np.random.normal(0, 2.5, self.n))
        fare_obs = np.clip(fare_obs, 0, None).round(2)"""
            )
            
            # Inject into dataframe
            source = source.replace(
                "'fare_rand': fare_rand",
                "'treatment_obs': treatment_obs,\n            'y_obs': y_obs,\n            'fare_obs': fare_obs,\n            'fare_rand': fare_rand"
            )
            
            lines = [line + '\n' for line in source.split('\n')]
            if lines:
                lines[-1] = lines[-1].rstrip('\n')
            cell['source'] = lines
            break

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
