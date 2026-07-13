import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'
pdf_path = os.path.join(repoDir, 'pdfs', '162_Thi Ha Soe.pdf')
doc = fitz.open(pdf_path)
print(f'Pages: {len(doc)}, size: {doc[0].rect.width:.0f}x{doc[0].rect.height:.0f}')

# 全ページ全画像を列挙
for pno in range(min(3, len(doc))):
    page = doc[pno]
    imgs = page.get_images(full=True)
    print(f'  Page {pno}: {len(imgs)} images')
    for i, img_info in enumerate(imgs):
        xref = img_info[0]
        try:
            base = doc.extract_image(xref)
            w, h = base['width'], base['height']
            ratio = h / max(w, 1)
            area = w * h
            is_face = 0.7 <= ratio <= 2.2 and 5000 < area < 500000
            print(f'    img[{i}]: {w}x{h} ratio={ratio:.2f} area={area} face={is_face} ext={base["ext"]}')
        except Exception as e:
            print(f'    img[{i}]: error {e}')

# プレビュー保存
page = doc[0]
pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
pix.save(os.path.join(workspace, 'prev_162.png'))
print('preview saved')
doc.close()
