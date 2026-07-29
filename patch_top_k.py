import json
import sys

nb_path = 'notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = cell['source']
        if isinstance(source, list):
            source_str = "".join(source)
        else:
            source_str = source
            
        if "k_revenue = k_trips * profit_per_ride" in source_str:
            if "top_k = df_res.sort_values" not in source_str:
                source_str = source_str.replace(
                    "    k_revenue = k_trips * profit_per_ride\n",
                    "    k_revenue = k_trips * profit_per_ride\n    top_k = df_res.sort_values(by='CATE_pred', ascending=False).iloc[:threshold_idx]\n"
                )
                
        if isinstance(cell['source'], list):
            cell['source'] = source_str.splitlines(True)
        else:
            cell['source'] = source_str

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
