import json
import sys

nb_path = 'notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb'

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
except Exception as e:
    print(f"Error loading notebook: {e}")
    sys.exit(1)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = cell['source']
        if isinstance(source, list):
            source = "".join(source)
            
        # Patch Expected Profit calculation
        if 'voucher_cost = 15000' in source:
            source = source.replace(
                "voucher_cost = 15000\n",
                "discount_rate = 0.25\n"
            )
            source = source.replace(
                "df_res['Expected_Profit'] = (df_res['CATE_pred'] * profit_per_ride) - voucher_cost",
                "df_res['Expected_Profit'] = (0.75 * df_res['CATE_pred'] * profit_per_ride) - (0.25 * df_res['monthly_rides_history'] * profit_per_ride)"
            )
            source = source.replace(
                "break_even_cate = voucher_cost / profit_per_ride",
                "break_even_cate = (0.25 * df_res['monthly_rides_history'].mean()) / 0.75"
            )
            
        # Patch Actual Profit calculation for Mass Campaign
        if 'mass_profit = (mass_trips * profit_per_ride) - (mass_vouchers * voucher_cost)' in source:
            source = source.replace(
                "mass_profit = (mass_trips * profit_per_ride) - (mass_vouchers * voucher_cost)",
                "mass_profit = (0.75 * mass_trips * profit_per_ride) - (0.25 * df_res['monthly_rides_history'].sum() * profit_per_ride)"
            )
            
        # Patch Actual Profit calculation for Top-K Campaign
        if 'k_cost = k_vouchers * voucher_cost' in source:
            source = source.replace(
                "    k_cost = k_vouchers * voucher_cost\n",
                "    k_cost = 0.25 * (top_k['y_true'] + top_k['monthly_rides_history']).sum() * profit_per_ride\n"
            )
            source = source.replace(
                "    k_profit = k_revenue - k_cost\n",
                "    k_profit = (0.75 * top_k['y_true'].sum() * profit_per_ride) - (0.25 * top_k['monthly_rides_history'].sum() * profit_per_ride)\n"
            )
            
        # Convert back to list of lines for Jupyter format if needed (not strictly required for jupyter, but good practice)
        if isinstance(cell['source'], list):
            # Split by newline but keep the newline character
            lines = source.splitlines(True)
            cell['source'] = lines
        else:
            cell['source'] = source

try:
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Successfully patched Week 7 Notebook logic!")
except Exception as e:
    print(f"Error saving notebook: {e}")
