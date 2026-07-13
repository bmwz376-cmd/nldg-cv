import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')

targets = [
    '159_Lae Yi Win.pdf',
    '160_Thuzar Myint.pdf',
    '161_Aye Thandar Aung.pdf',
]

for pdf_name in targets:
    pdf_path = os.path.join(pdf_dir, pdf_name)
    if not os.path.exists(pdf_path):
        print(f'NOT FOUND: {pdf_name}')
        continue
    doc = fitz.open(pdf_path)
    print(f'=== {pdf_name} ({len(doc)} pages) ===')
    for pno in range(min(3, len(doc))):
        page = doc[pno]
        imgs = page.get_images(full=True)
        print(f'  Page {pno}: {len(imgs)} images')
        for i, img_info in enumerate(imgs):
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                w, h = base['width'], base['height']
                area = w * h
                ratio = h / max(w, 1)
                ext = base['ext']
                print(f'    img[{i}]: {w}x{h} ratio={ratio:.2f} area={area} ext={ext}')
            except Exception as e:
                print(f'    img[{i}]: error {e}')
    doc.close()
