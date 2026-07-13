# -*- coding: utf-8 -*-
import json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# v2データ読み込み（学部なし=other）
with open(os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'dept_results_v2.json'), encoding='utf-8') as f:
    data = json.load(f)

dept_map = {d['no']: d['cat'] for d in data}

# 118 Shwe Wuit Yee Oo は Mechatronics と明記 → mechanical に戻す
dept_map[118] = 'mechanical'

# index.html 読み込み
with open(os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'index.html'), encoding='utf-8') as f:
    html = f.read()

# candidates配列の各エントリの dept を更新
def update_dept(m):
    entry = m.group(0)
    no_m = re.search(r'no:(\d+)', entry)
    if not no_m: return entry
    no = int(no_m.group(1))
    new_cat = dept_map.get(no, 'other')
    # 既存のdept値を置換
    entry = re.sub(r',dept:"[^"]*"', f',dept:"{new_cat}"', entry)
    return entry

new_html = re.sub(r'\{no:\d+,[^}]+\}', update_dept, html)

# build meta更新
from datetime import datetime
now = datetime.now().strftime('%Y%m%d-%H%M')
new_html = re.sub(r'content="20\d{6}-\d{4}"', f'content="{now}"', new_html)

with open(os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(new_html)

# 変更確認
from collections import Counter
cats_new = Counter(dept_map.values())
print('=== 最終分類（更新後）===')
for cat in ['civil','architecture','electrical','mechanical','it','other']:
    print(f'  {cat:15s}: {cats_new[cat]}件')
print(f'  合計: {sum(cats_new.values())}件')

# 変更があった件数
changed = sum(1 for no, cat in dept_map.items() if cat != {d['no']:d['cat'] for d in json.load(open(os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv','dept_results.json'),encoding='utf-8'))}.get(no))
print(f'\n変更件数: {changed}件')
