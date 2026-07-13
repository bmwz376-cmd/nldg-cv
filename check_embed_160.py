import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 159: 709x945 (PNG) はページ全体なのでスキップ → クロップ使用
# 160: 155x187 (JPEG) は顔写真だが低解像度 → そのまま使用 or クロップ比較
# 161: 260x315 (JPEG) は顔写真 OK → 直接使用

# 160の埋め込み画像を確認
pdf160 = os.path.join(pdf_dir, '160_Thuzar Myint.pdf')
doc = fitz.open(pdf160)
for pno in range(min(2, len(doc))):
    page = doc[pno]
    for i, img_info in enumerate(page.get_images(full=True)):
        xref = img_info[0]
        base = doc.extract_image(xref)
        w, h = base['width'], base['height']
        ext = base['ext']
        print(f'160 p{pno} img[{i}]: {w}x{h} ext={ext}')
        if 0.7 <= h/max(w,1) <= 2.0 and w*h > 5000:
            p = os.path.join(workspace, f'160_embed_{i}.{ext}')
            with open(p,'wb') as f: f.write(base['image'])
            print(f'  saved: {p} ({os.path.getsize(p)}B)')
doc.close()

# 161の埋め込みを最終写真として保存
pdf161 = os.path.join(pdf_dir, '161_Aye Thandar Aung.pdf')
doc = fitz.open(pdf161)
base = doc.extract_image(doc[0].get_images(full=True)[0][0])
out = os.path.join(out_dir, '161_Aye Thandar Aung.jpg')
with open(out, 'wb') as f: f.write(base['image'])
print(f'161 final: {os.path.getsize(out)}B')
doc.close()
