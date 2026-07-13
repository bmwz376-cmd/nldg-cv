import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')

targets = [
    ('162_Thi Ha Soe.pdf', '162_Thi Ha Soe.jpg'),
    ('163_Tin Moh Moh Oo.pdf', '163_Tin Moh Moh Oo.jpg'),
    ('164_Pan Lae Lae Mon.pdf', '164_Pan Lae Lae Mon.jpg'),
    ('165_Nay Hlaing Tun.pdf', '165_Nay Hlaing Tun.jpg'),
    ('166_Thein Htaik Soe.pdf', '166_Thein Htaik Soe.jpg'),
    ('167_Zaw Htwe Aung.pdf', '167_Zaw Htwe Aung.jpg'),
    ('168_Kaung Htet Lin.pdf', '168_Kaung Htet Lin.jpg'),
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
    if best and best_score > 5000:
        with open(out_path, 'wb') as f: f.write(best)
        return os.path.getsize(out_path)
    # フォールバック: ページ上部をレンダリング
    doc2 = fitz.open(pdf_path)
    page = doc2[0]
    clip = fitz.Rect(0, 0, page.rect.width * 0.45, page.rect.height * 0.38)
    pix = page.get_pixmap(matrix=fitz.Matrix(2,2), clip=clip)
    pix.save(out_path)
    doc2.close()
    return os.path.getsize(out_path)

for pdf_name, jpg_name in targets:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    out_path = os.path.join(out_dir, jpg_name)
    if not os.path.exists(pdf_path):
        print(f'SKIP (not found): {pdf_name}')
        continue
    size = extract_best(pdf_path, out_path)
    print(f'OK {jpg_name}: {size} bytes')
