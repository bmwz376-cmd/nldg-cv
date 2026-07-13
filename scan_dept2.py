import fitz, os, json, re

pdf_dir = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'pdfs')

CATEGORY_MAP = {
    'civil':        ['civil engineering','civil engi','c.e.','land surveying','surveying','geotechnical','highway','water supply','drainage','irrigation','structural','soil mechanics'],
    'architecture': ['architect','architecture','interior design','urban planning','town planning','building design'],
    'electrical':   ['electrical engineering','electronic engineering','electronics','power engineering','telecommunication','telecom','electrical & electronic','eee','ece'],
    'mechanical':   ['mechanical engineering','mechatronics','industrial engineering','automotive engineering','machine design'],
    'it':           ['information technology','computer science','software engineering','computer engineering','information system','information & communication'],
    'other':        [],
}

def classify(text):
    t = text.lower()
    for cat, keywords in CATEGORY_MAP.items():
        if cat == 'other': continue
        for kw in keywords:
            if kw in t:
                idx = t.find(kw)
                context = t[max(0,idx-80):idx+80]
                edu_words = ['university','college','degree','faculty','bachelor','department','engineering','school','graduate','major','institute','polytechnic','b.e','b.tech','b.sc','diploma','technology']
                if any(w in context for w in edu_words):
                    return cat, kw
    return None, None

results = []
unclassified = []

# 番号付きPDFのみ対象
pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf') and re.match(r'^\d{3}_', f)])
print(f'番号付きPDF: {len(pdfs)}件')

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
        if cat:
            results.append({'no': no, 'name': name, 'cat': cat, 'kw': kw})
        else:
            unclassified.append({'no': no, 'name': name, 'text_len': len(text), 'snippet': text[:120].replace(chr(10),' ')})
    except Exception as e:
        unclassified.append({'no': no, 'name': name, 'text_len': 0, 'snippet': f'ERROR:{e}'})

out_path = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'dept_classified.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({'classified': results, 'unclassified': unclassified}, f, ensure_ascii=False, indent=2)

print(f'分類済み: {len(results)}件')
print(f'未分類:   {len(unclassified)}件')

from collections import Counter
cnt = Counter(r['cat'] for r in results)
print('\nカテゴリ別:')
for cat, n in cnt.most_common():
    print(f'  {cat:15s}: {n}件')

print('\n=== 未分類（テキストあり）===')
for u in sorted(unclassified, key=lambda x: -x['text_len'])[:30]:
    print(f"  [{u['no']:03d}] {u['name']:<30s} text={u['text_len']:5d}  {u['snippet'][:60]}")
