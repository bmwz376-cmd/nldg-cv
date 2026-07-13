import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

targets = [
    (163, 'Tin Moh Moh Oo'),
    (164, 'Pan Lae Lae Mon'),
    (165, 'Nay Hlaing Tun'),
    (166, 'Thein Htaik Soe'),
]

for no, name in targets:
    pdf_path = os.path.join(pdf_dir, f'{no}_{name}.pdf')
    doc = fitz.open(pdf_path)
    # 1ページ目プレビュー
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    out = os.path.join(workspace, f'prev_{no}.png')
    pix.save(out)
    # 埋め込み画像一覧
    print(f'=== {no}_{name} (pages={len(doc)}, size={page.rect.width:.0f}x{page.rect.height:.0f}) ===')
    for pno in range(min(2, len(doc))):
        pg = doc[pno]
        for i, img_info in enumerate(pg.get_images(full=True)):
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                w, h = base['width'], base['height']
                ratio = h / max(w, 1)
                area = w * h
                is_face = 0.7 <= ratio <= 2.2 and 5000 < area < 500000
                print(f'  p{pno} img[{i}]: {w}x{h} ratio={ratio:.2f} face={is_face} ext={base["ext"]}')
            except Exception as e:
                print(f'  p{pno} img[{i}]: error {e}')
    doc.close()
    print(f'  -> preview: prev_{no}.png')
