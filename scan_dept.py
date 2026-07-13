import fitz, os, json, re

pdf_dir = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'pdfs')

# 学科キーワードマッピング
CATEGORY_MAP = {
    'civil':        ['civil', 'civil engineering', 'ce ', 'c.e.', 'construction', 'infrastructure', 'land surveying', 'surveying', 'geotechnical'],
    'architecture': ['architect', 'architecture', 'building', 'interior design', 'urban planning', 'town planning'],
    'electrical':   ['electrical', 'electronic', 'electronics', 'electric', 'power engineering', 'telecommunication', 'telecom', 'ece ', 'eee '],
    'mechanical':   ['mechanical', 'mechatronics', 'industrial engineering', 'automotive', 'machine', 'ep '],
    'it':           ['information technology', 'computer science', 'it ', 'software', 'computer engineering', 'information system', 'data', 'network'],
    'other':        [],
}

def classify(text):
    t = text.lower()
    for cat, keywords in CATEGORY_MAP.items():
        for kw in keywords:
            if kw in t:
                # 大学・学部っぽい文脈かチェック
                idx = t.find(kw)
                context = t[max(0,idx-60):idx+60]
                if any(w in context for w in ['university','college','degree','faculty','bachelor','department','engineering','school','graduated','major','institute','polytechnic','b.e','b.tech','b.sc']):
                    return cat, kw, context.strip()
    return None, None, None

results = []
unclassified = []

pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
print(f'Total PDFs: {len(pdfs)}')

for pdf_name in pdfs:
    path = os.path.join(pdf_dir, pdf_name)
    no_str = pdf_name.split('_')[0]
    name = pdf_name.replace(no_str+'_','').replace('.pdf','')
    
    try:
        doc = fitz.open(path)
        text = ''
        for pno in range(min(3, len(doc))):
            text += doc[pno].get_text()
        doc.close()
        
        cat, kw, ctx = classify(text)
        
        if cat:
            results.append({'no': int(no_str), 'name': name, 'cat': cat, 'kw': kw, 'ctx': ctx[:80]})
        else:
            # テキスト量も確認
            unclassified.append({'no': int(no_str), 'name': name, 'text_len': len(text), 'snippet': text[:100].replace('\n',' ')})
    except Exception as e:
        unclassified.append({'no': int(no_str), 'name': name, 'text_len': 0, 'snippet': f'ERROR: {e}'})

# 結果保存
out_path = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'dept_classified.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'classified': results, 'unclassified': unclassified}, f, ensure_ascii=False, indent=2)

print(f'\n分類済み: {len(results)}件')
print(f'未分類:   {len(unclassified)}件')

# カテゴリ別集計
from collections import Counter
cnt = Counter(r['cat'] for r in results)
for cat, n in cnt.most_common():
    print(f'  {cat}: {n}件')

print('\n=== 未分類の上位20件 ===')
for u in unclassified[:20]:
    print(f"  [{u['no']:03d}] {u['name']}  text={u['text_len']}  {u['snippet'][:60]}")
