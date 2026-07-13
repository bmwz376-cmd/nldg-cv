# -*- coding: utf-8 -*-
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# 手動分類（未分類16件）
manual = {
    1:   'civil',         # タンリン工科大学（土木系）
    10:  'electrical',    # Chindwin Technology University B.E → 電気系
    56:  'other',         # 造船工学 → その他
    61:  'other',         # 化学専攻 → その他
    63:  'other',         # 化学専攻（同一人物）→ その他
    68:  'other',         # 学部記載なし → その他
    69:  'other',         # Economics → その他
    70:  'other',         # Botany（理学）→ その他
    71:  'other',         # 記載なし → その他
    72:  'other',         # 記載なし → その他
    73:  'other',         # 理学 → その他
    74:  'other',         # 記載なし → その他
    95:  'other',         # BBA（経営）→ その他
    115: 'other',         # 冶金学 → その他
    118: 'mechanical',    # Mechatronics → 機械
    119: 'other',         # 化学工学 → その他
}

results_path = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'dept_results.json')
with open(results_path, encoding='utf-8') as f:
    results = json.load(f)

# 手動分類を上書き
for item in results:
    no = item['no']
    if no in manual:
        item['cat'] = manual[no]
        item['kw'] = 'manual'

# 最終集計
from collections import Counter
cnt = Counter(item['cat'] for item in results)
print('=== 最終分類結果 ===')
for cat in ['civil','architecture','electrical','mechanical','it','other']:
    print(f'  {cat:15s}: {cnt.get(cat,0)}件')
print(f'  合計: {len(results)}件')

# 保存
with open(results_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('saved:', results_path)
