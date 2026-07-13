import fitz, os, re

pdf_dir = os.path.join(r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv', 'pdfs')

# サンプル10件のテキストを出力
samples = ['008_Hsu Mon Aung.pdf','011_Thwe Mon Oo.pdf','021_Shwin Lai Tun.pdf','038_Thet Myat Noe Oo.pdf','050_YE NAING SOE.pdf']

for pdf_name in samples:
    path = os.path.join(pdf_dir, pdf_name)
    if not os.path.exists(path): continue
    doc = fitz.open(path)
    text = ''
    for pno in range(min(3, len(doc))):
        text += doc[pno].get_text()
    doc.close()
    print(f'=== {pdf_name} ===')
    # 学歴っぽい部分を抽出
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for i, line in enumerate(lines):
        if any(kw in line for kw in ['大学','学部','学科','工学','建築','土木','電気','機械','情報','University','College','Engineering','Faculty','Department','Bachelor','degree']):
            # 前後の行も表示
            start = max(0, i-1)
            end = min(len(lines), i+3)
            for l in lines[start:end]:
                print(f'  >> {l}')
            print()
    print()
