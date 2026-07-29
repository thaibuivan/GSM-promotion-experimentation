import json
import sys

nb_path = 'notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = cell['source']
        if isinstance(source, list):
            source = "".join(source)
            
        if 'cost = n_treated * voucher_cost' in source:
            source = source.replace(
                "    cost = n_treated * voucher_cost\n",
                "    cost = 0.25 * (y_target[t_target == 1] + df_res.loc[positive_cate_mask, 'monthly_rides_history'][t_target == 1]).sum() * profit_per_ride\n"
            )
            
        if isinstance(cell['source'], list):
            cell['source'] = source.splitlines(True)
        else:
            cell['source'] = source

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
