import fitz, os, json

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')

def is_face_photo(w, h):
    area = w * h
    ratio = h / max(w, 1)
    return 0.7 <= ratio <= 2.5 and 5000 < area < 400000

def is_full_page(w, h):
    return w * h > 300000

def get_page_render_crop(pdf_path, out_path, zoom=3):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pw = page.rect.width
    ph = page.rect.height
    # 顔写真は右上か左上に多い - まず右上、なければ左上を試す
    # 一般的な履歴書レイアウト: 右上に顔写真
    clips = [
        fitz.Rect(pw * 0.55, 0, pw, ph * 0.35),   # 右上
        fitz.Rect(0, 0, pw * 0.45, ph * 0.38),     # 左上
    ]
    best_path = out_path
    mat = fitz.Matrix(zoom, zoom)
    # まず右上を試す
    pix = page.get_pixmap(matrix=mat, clip=clips[0])
    pix.save(out_path)
    doc.close()
    size = os.path.getsize(out_path)
    return size

targets = [
    ('159_Lae Yi Win.pdf', '159_Lae Yi Win.jpg', True),   # ページ全体画像なのでクロップ必須
    ('160_Thuzar Myint.pdf', '160_Thuzar Myint.jpg', False), # 小さい顔写真あり
    ('161_Aye Thandar Aung.pdf', '161_Aye Thandar Aung.jpg', False), # 顔写真あり
]

for pdf_name, jpg_name, force_crop in targets:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    out_path = os.path.join(out_dir, jpg_name)
    doc = fitz.open(pdf_path)
    
    if not force_crop:
        # 顔写真として抽出を試みる
        best = None
        best_score = 0
        for pno in range(min(2, len(doc))):
            page = doc[pno]
            for img_info in page.get_images(full=True):
                xref = img_info[0]
                try:
                    base = doc.extract_image(xref)
                    w, h = base['width'], base['height']
                    if is_full_page(w, h): continue
                    if is_face_photo(w, h):
                        score = w * h
                        if score > best_score:
                            best_score = score
                            best = base['image']
                except: pass
        doc.close()
        
        if best:
            with open(out_path, 'wb') as f: f.write(best)
            sz = os.path.getsize(out_path)
            print(f'EXTRACTED {jpg_name}: {sz}B ({int(best_score**0.5)}px~)')
            continue
        else:
            print(f'No face found in {pdf_name}, falling back to crop')
    else:
        doc.close()
    
    # クロップフォールバック（右上 → 左上）
    doc2 = fitz.open(pdf_path)
    page = doc2[0]
    pw, ph = page.rect.width, page.rect.height
    mat = fitz.Matrix(3, 3)
    for label, clip in [('right-top', fitz.Rect(pw*0.55, 0, pw, ph*0.35)),
                        ('left-top',  fitz.Rect(0, 0, pw*0.45, ph*0.38))]:
        pix = page.get_pixmap(matrix=mat, clip=clip)
        pix.save(out_path)
        sz = os.path.getsize(out_path)
        print(f'CROP({label}) {jpg_name}: {sz}B')
        break   # まず右上を採用
    doc2.close()
