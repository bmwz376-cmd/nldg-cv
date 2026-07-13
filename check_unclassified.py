# -*- coding: utf-8 -*-
import fitz, os, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'pdfs')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 未分類16件のテキストから学歴部分を抽出
unclassified_nos = [1,10,56,61,63,68,69,70,71,72,73,74,95,115,118,119]
names = {
    1:'Kyo Tagoo Naing',10:'Ku Ku Myat',56:'CV',61:'KHIN KHIN THI',63:'khin Khin Thi cv',
    68:'Aung Myo Oo',69:'La Min Soe',70:'Phoo Myat Kay Khaing',71:'Si Thu Min Htet',
    72:'Swan Gone Yee',73:'Tin Nilar Myo',74:'Zin Min Htet',95:'Htet Aung Aung',
    115:'Pyae Phyo Ko Ko',118:'Shwe Wuit Yee Oo',119:'Hlaing Bwar Aung'
}

import glob
all_pdfs = {int(f[:3]): os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf') and f[:3].isdigit()}

for no in unclassified_nos:
    path = all_pdfs.get(no)
    if not path or not os.path.exists(path): print(f'[{no:03d}] FILE NOT FOUND'); continue
    doc = fitz.open(path)
    text = ''
    for pno in range(min(3, len(doc))):
        text += doc[pno].get_text()
    doc.close()
    # 学歴行を探す
    edu_hits = []
    for line in text.split('\n'):
        line = line.strip()
        if len(line) < 3: continue
        if any(kw in line for kw in ['大学','工科','工業','学部','学科','University','College','Engineering','Faculty','Bachelor','Institute','Technology','Polytechnic','Department']):
            edu_hits.append(line)
    print(f'[{no:03d}] {names.get(no,"")}')
    for h in edu_hits[:5]:
        print(f'  {h[:80]}')
    if not edu_hits:
        print(f'  (学歴行なし) text={len(text)}文字')
    print()
