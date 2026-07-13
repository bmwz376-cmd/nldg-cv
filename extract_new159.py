import fitz, os, sys

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')

targets = [
    ('159_Lae Yi Win.pdf', '159_Lae Yi Win.jpg'),
    ('160_Thuzar Myint.pdf', '160_Thuzar Myint.jpg'),
    ('161_Aye Thandar Aung.pdf', '161_Aye Thandar Aung.jpg'),
]

def is_face_photo(w, h):
    area = w * h
    ratio = h / max(w, 1)
    return 0.7 <= ratio <= 2.5 and 2500 < area < 500000

def is_full_page(w, h):
    return w * h > 3000000 or (w > 1500 and h > 2000)

def extract_best(pdf_path, out_path):
    doc = fitz.open(pdf_path)
    best = None
    best_score = 0
    for pno in range(min(2, len(doc))):
        page = doc[pno]
        imgs = page.get_images(full=True)
        for img_info in imgs:
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                w, h = base['width'], base['height']
                if is_full_page(w, h):
                    continue
                if is_face_photo(w, h):
                    score = w * h
                    if score > best_score:
                        best_score = score
                        best = base['image']
                        print(f'  Candidate image: {w}x{h} score={score}')
            except Exception as e:
                pass
    doc.close()
    if best:
        with open(out_path, 'wb') as f:
            f.write(best)
        print(f'  -> Saved: {os.path.basename(out_path)}')
        return True
    else:
        print(f'  -> No face photo found, using page render fallback')
        # フォールバック: ページをレンダリングして上部をクロップ
        doc2 = fitz.open(pdf_path)
        page = doc2[0]
        mat = fitz.Matrix(2, 2)
        clip = fitz.Rect(0, 0, page.rect.width * 0.45, page.rect.height * 0.35)
        pix = page.get_pixmap(matrix=mat, clip=clip)
        pix.save(out_path)
        doc2.close()
        print(f'  -> Fallback saved: {os.path.basename(out_path)}')
        return True

for pdf_name, jpg_name in targets:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    out_path = os.path.join(out_dir, jpg_name)
    print(f'Processing: {pdf_name}')
    if not os.path.exists(pdf_path):
        print(f'  ERROR: PDF not found: {pdf_path}')
        continue
    extract_best(pdf_path, out_path)
    if os.path.exists(out_path):
        size = os.path.getsize(out_path)
        print(f'  File size: {size} bytes')

print('Done.')
