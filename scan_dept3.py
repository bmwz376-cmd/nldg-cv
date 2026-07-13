# -*- coding: utf-8 -*-
import fitz, os, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'pdfs')

# 日本語＋英語両対応キーワードマッピング
CATEGORY_MAP = {
    'civil': [
        # 日本語
        '土木','建設工学','建設学','道路','橋梁','河川','上下水道','測量','地盤',
        # ミャンマー語ローマ字/英語
        'civil engineering','civil engi','construction engineering',
        'land surveying','surveying','geotechnical','highway','water supply',
        'drainage','irrigation','structural engineering',
    ],
    'architecture': [
        # 日本語
        '建築','インテリア','都市計画','住宅',
        # 英語
        'architect','architecture','interior design','urban planning','town planning','building design',
    ],
    'electrical': [
        # 日本語
        '電気','電子','電力','通信工学','情報通信',
        # 英語
        'electrical engineering','electronic engineering','electronics',
        'power engineering','telecommunication','telecom','electrical & electronic','eee','ece',
    ],
    'mechanical': [
        # 日本語
        '機械','メカトロ','自動車工学','産業工学',
        # 英語
        'mechanical engineering','mechatronics','industrial engineering',
        'automotive engineering','machine design',
    ],
    'it': [
        # 日本語
        '情報技術','情報工学','コンピュータ','ソフトウェア','情報システム',
        # 英語
        'information technology','computer science','software engineering',
        'computer engineering','information system','information & communication',
    ],
}

# 学歴文脈キーワード（日本語＋英語）
EDU_CONTEXT = [
    '大学','工科大','工業大','大学院','専門学校','学部','学科','卒業','修了',
    'university','college','degree','faculty','bachelor','department',
    'engineering','school','graduate','major','institute','polytechnic',
    'b.e','b.tech','b.sc','diploma','technology',
]

def classify(text):
    t_lower = text.lower()
    # 学歴部分を重点的に探す
    for cat, keywords in CATEGORY_MAP.items():
        for kw in keywords:
            kw_lower = kw.lower()
            # テキスト内の全出現位置を確認
            idx = 0
            while True:
                pos = t_lower.find(kw_lower, idx)
                if pos == -1: break
                context = text[max(0,pos-100):pos+100]
                context_lower = context.lower()
                if any(ew in context_lower for ew in EDU_CONTEXT):
                    return cat, kw
                idx = pos + 1
    return None, None

# 番号付きPDFのみ対象
pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf') and re.match(r'^\d{3}_', f)])

results = {}
unclassified = []

for pdf_name in pdfs:
    path = os.path.join(pdf_dir, pdf_name)
    m = re.match(r'^(\d{3})_(.*?)\.pdf$', pdf_name)
    if not m: continue
    no = int(m.group(1))
    name = m.group(2)

    try:
        doc = fitz.open(path)
        text = ''
        for pno in range(min(4, len(doc))):
            text += doc[pno].get_text()
        doc.close()

        cat, kw = classify(text)
        results[no] = {'no': no, 'name': name, 'cat': cat, 'kw': kw if kw else ''}
        if not cat:
            unclassified.append({'no': no, 'name': name})
    except Exception as e:
        results[no] = {'no': no, 'name': name, 'cat': None, 'kw': ''}
        unclassified.append({'no': no, 'name': name, 'err': str(e)})

out_path = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'dept_results.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(list(results.values()), f, ensure_ascii=False, indent=2)

from collections import Counter
cats = [v['cat'] for v in results.values()]
cnt = Counter(cats)
print(f'分類済み: {len(results) - cnt[None]}件 / {len(results)}件')
print()
for cat in ['civil','architecture','electrical','mechanical','it',None]:
    label = cat if cat else '未分類'
    print(f'  {label:15s}: {cnt[cat]}件')

print(f'\n未分類 {len(unclassified)}件:')
for u in unclassified:
    print(f'  [{u["no"]:03d}] {u["name"]}')
