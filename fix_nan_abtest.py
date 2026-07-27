import json

# --- SỬA NOTEBOOK 3: Cập nhật lại auto_label và Markdown ---
file3 = r'D:\Intern VSF\GSM-promotion-experimentation\notebooks\week3_segmentation\1_user_segmentation.ipynb'
with open(file3, 'r', encoding='utf-8') as f:
    nb3 = json.load(f)

for cell in nb3['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        for line in source:
            if "if row['payment_type'] > 1.5:" in line:
                continue
            if "if row['is_weekend_rider'] > 0.5 and row['is_urban'] > 0.5:" in line:
                new_source.append("    if row['is_urban'] < 0.3:                                      return 'Suburban Occasionals'\n")
                new_source.append("    if row['is_rain_rider'] > 0.5:                                 return 'Rain Riders'\n")
                new_source.append("    if row['is_rush_hour'] > 0.5:                                  return 'Urban Regulars'\n")
                new_source.append("    return 'Urban Leisure'\n")
                continue
            if "if row['is_urban'] > 0.5:                                      return 'Urban Regulars'" in line:
                continue
            if "return 'Suburban Occasionals'" in line and "if row['is_urban'] < 0.3" not in ''.join(new_source):
                continue
            new_source.append(line)
        cell['source'] = new_source

    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        if "Cash Traditional" in source:
            cell['source'] = [
                "### Định nghĩa 5 Business Personas Thực Tế (Khám phá bởi K-Means)\n\n",
                "Dựa vào Centroid, K-Means đã tự động gom nhóm 20,000 khách hàng thành 5 Personas tự nhiên nhất dựa trên hành vi:\n\n",
                "| Persona | Đặc điểm nổi bật | Tần suất | Độ nhạy Voucher |\n",
                "|---|---|---|---|\n",
                "| **Airport Business** | Chuyến đi sân bay, fare cao 3-4x, giờ cố định theo lịch bay | ~5% | ❌ Kháng hoàn toàn (ATE≈0) |\n",
                "| **Rain Riders** | Chỉ thích đi xe khi trời mưa (phụ thuộc thời tiết) | ~14% | ✅ Rất cao |\n",
                "| **Urban Leisure** | Nội thành, giờ thấp điểm (không vội) | ~27% | ✅ Cao |\n",
                "| **Urban Regulars** | Nội thành, giờ cao điểm (đi làm hàng ngày) | ~20% | ❌ Thấp (kiểu gì cũng đi) |\n",
                "| **Suburban Occasionals** | Ngoại ô, thỉnh thoảng mới đi | ~33% | ✅ Trung bình |\n"
            ]

with open(file3, 'w', encoding='utf-8') as f:
    json.dump(nb3, f, indent=1, ensure_ascii=False)


# --- SỬA NOTEBOOK 4: Cập nhật danh sách test ---
file4 = r'D:\Intern VSF\GSM-promotion-experimentation\notebooks\week4_ab_testing\1_ab_test_analysis.ipynb'
with open(file4, 'r', encoding='utf-8') as f:
    nb4 = json.load(f)

for cell in nb4['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        for line in source:
            if "personas_to_test = [" in line:
                new_source.append("personas_to_test = ['Airport Business', 'Rain Riders', 'Urban Leisure', 'Urban Regulars', 'Suburban Occasionals']\n")
            elif "sns.barplot(x=personas_to_test" in line:
                new_source.append("    sns.barplot(x=personas_to_test, y=rois, palette=['#e74c3c', '#2ecc71', '#3498db', '#f1c40f', '#9b59b6'])\n")
            else:
                new_source.append(line)
        cell['source'] = new_source

with open(file4, 'w', encoding='utf-8') as f:
    json.dump(nb4, f, indent=1, ensure_ascii=False)

print("Patch done!")
