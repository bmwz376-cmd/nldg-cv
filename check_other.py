# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv\dept_results.json', encoding='utf-8') as f:
    data = json.load(f)

print('現在の「その他」分類:')
for d in sorted(data, key=lambda x: x['no']):
    if d['cat'] == 'other':
        print(f"  [{d['no']:03d}] {d['name']}  kw={d['kw']}")
