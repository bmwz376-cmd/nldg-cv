import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_path = os.path.join(repoDir, 'pdfs', '169_Phyo Hein Kyaw.pdf')
out_path = os.path.join(repoDir, 'photos', '169_Phyo Hein Kyaw.jpg')
ws_path  = os.path.join(r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace', 'crop_169.jpg')

doc = fitz.open(pdf_path)
page = doc[0]
pw, ph = page.rect.width, page.rect.height

# Vision AI座標: x0=0.77 y0=0.12 x1=0.92 y1=0.25 (枠内側に少し絞る)
clip = fitz.Rect(pw*0.78, ph*0.125, pw*0.915, ph*0.245)
pix  = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip)
pix.save(out_path)
pix.save(ws_path)
doc.close()
print(f'OK: {os.path.getsize(out_path)}B  pix={pix.width}x{pix.height}')
