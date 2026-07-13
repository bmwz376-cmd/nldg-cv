# -*- coding: utf-8 -*-
import fitz, os, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'pdfs')

CATEGORY_MAP = {
    'civil': ['土木','建設工学','建設学','道路','橋梁','河川','上下水道','測量','地盤','civil engineering','civil engi','construction engineering','land surveying','surveying','geotechnical','highway','water supply','drainage','irrigation','structural engineering'],
    'architecture': ['建築','インテリア','都市計画','住宅','architect','architecture','interior design','urban planning','town planning','building design'],
    'electrical': ['電気','電子','電力','通信工学','情報通信','electrical engineering','electronic engineering','electronics','power engineering','telecommunication','telecom','electrical & electronic','eee','ece'],
    'mechanical': ['機械','メカトロ','自動車工学','産業工学','mechanical engineering','mechatronics','industrial engineering','automotive engineering','machine design'],
    'it': ['情報技術','情報工学','コンピュータ','ソフトウェア','情報システム','information technology','computer science','software engineering','computer engineering','information system'],
}
EDU_CONTEXT = ['大学','工科大','工業大','大学院','専門学校','学部','学科','卒業','修了','university','college','degree','faculty','bachelor','department','engineering','school','graduate','major','institute','polytechnic','b.e','b.tech','b.sc','diploma','technology']

def classify_strict(text):
    """学歴文脈内にキーワードがある場合のみ分類、それ以外はNone"""
    t_lower = text.lower()
    for cat, keywords in CATEGORY_MAP.items():
        for kw in keywords:
            kw_lower = kw.lower()
            idx = 0
            while True:
                pos = t_lower.find(kw_lower, idx)
                if pos == -1: break
                context = text[max(0,pos-100):pos+100]
                context_lower = context.lower()
                if any(ew in context_lower for ew in EDU_CONTEXT):
                    return cat, kw, context.strip()[:80]
                idx = pos + 1
    return None, None, None

pdfs = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf') and re.match(r'^\d{3}_', f)])

results = []
for pdf_name in pdfs:
    path = os.path.join(pdf_dir, pdf_name)
    m = re.match(r'^(\d{3})_(.*?)\.pdf$', pdf_name)
    if not m: continue
    no, name = int(m.group(1)), m.group(2)
    try:
        doc = fitz.open(path)
        text = ''.join(doc[pno].get_text() for pno in range(min(4, len(doc))))
        doc.close()
        cat, kw, ctx = classify_strict(text)
        results.append({'no':no,'name':name,'cat':cat,'kw':kw or '','ctx':ctx or ''})
    except Exception as e:
        results.append({'no':no,'name':name,'cat':None,'kw':'','ctx':f'ERROR:{e}'})

# 分類できなかった（=学部記載なし or 判定不能）
no_dept = [r for r in results if r['cat'] is None]
has_dept = [r for r in results if r['cat'] is not None]

from collections import Counter
cnt = Counter(r['cat'] for r in results)
print('=== 再スキャン結果 ===')
for cat in ['civil','architecture','electrical','mechanical','it',None]:
    label = cat if cat else '学部記載なし→その他'
    print(f'  {label:25s}: {cnt[cat]}件')

print(f'\n学部記載なし {len(no_dept)}件:')
for r in sorted(no_dept, key=lambda x: x['no']):
    print(f"  [{r['no']:03d}] {r['name']}")

# 結果保存
out = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'dept_results_v2.json')
# 学部なしは other に
for r in results:
    if r['cat'] is None:
        r['cat'] = 'other'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'\nsaved: {out}')
