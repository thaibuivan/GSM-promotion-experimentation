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
            
        if "df_res = pd.DataFrame({" in source_str:
            if "'monthly_rides_history':" not in source_str:
                source_str = source_str.replace(
                    "    'CATE_pred': cate_pred\n",
                    "    'CATE_pred': cate_pred,\n    'monthly_rides_history': X_test['monthly_rides_history'].values\n"
                )
                
        # Also need to make sure top_k has monthly_rides_history if it doesn't already, but top_k is derived from df_qini or df_res.
        # Let's check where top_k is created. It's probably top_k = df_res.iloc[:threshold_idx]. Oh wait! 
        # In the original code, top_k is NOT defined in that loop in my previous regex. Wait, it might be. Let's fix df_res first.
        
        if isinstance(cell['source'], list):
            cell['source'] = source_str.splitlines(True)
        else:
            cell['source'] = source_str

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
