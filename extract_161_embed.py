import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 161の埋め込み画像を全ページから抽出して確認
pdf_path = os.path.join(pdf_dir, '161_Aye Thandar Aung.pdf')
doc = fitz.open(pdf_path)
print(f'Pages: {len(doc)}')
for pno in range(len(doc)):
    page = doc[pno]
    imgs = page.get_images(full=True)
    for i, img_info in enumerate(imgs):
        xref = img_info[0]
        base = doc.extract_image(xref)
        w, h = base['width'], base['height']
        ext = base['ext']
        area = w * h
        ratio = h / max(w, 1)
        is_face = 0.7 <= ratio <= 2.0 and 5000 < area < 500000
        print(f'  p{pno} img[{i}]: {w}x{h} ratio={ratio:.2f} area={area} ext={ext} face={is_face}')
        if is_face:
            out_name = f'161_embed_p{pno}_img{i}.{ext}'
            out_p = os.path.join(workspace, out_name)
            with open(out_p, 'wb') as f: f.write(base['image'])
            print(f'    -> saved: {out_name} {os.path.getsize(out_p)}B')
doc.close()
