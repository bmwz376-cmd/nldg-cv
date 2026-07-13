import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_path = os.path.join(repoDir, 'pdfs', '169_Phyo Hein Kyaw.pdf')
out_path = os.path.join(repoDir, 'photos', '169_Phyo Hein Kyaw.jpg')
ws_path  = os.path.join(r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace', 'crop2_169.jpg')

doc = fitz.open(pdf_path)
page = doc[0]
pw, ph = page.rect.width, page.rect.height

# 左右の余白を除くためx0を右に、x1を左に絞る
clip = fitz.Rect(pw*0.795, ph*0.127, pw*0.900, ph*0.243)
pix  = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip)
pix.save(out_path)
pix.save(ws_path)
doc.close()
print(f'OK: {os.path.getsize(out_path)}B  pix={pix.width}x{pix.height}')
