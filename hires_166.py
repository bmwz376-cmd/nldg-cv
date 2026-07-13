import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'

# 166は元PDF埋め込み画像が133x156と低解像度 → ページレンダリングをzoom=8で高解像度化
pdf166 = os.path.join(pdf_dir, '166_Thein Htaik Soe.pdf')
doc = fitz.open(pdf166)
page = doc[0]
pw, ph = page.rect.width, page.rect.height

# zoom=8で高解像度レンダリング（枠内のみ）
clip = fitz.Rect(pw*0.412, ph*0.100, pw*0.473, ph*0.205)
pix = page.get_pixmap(matrix=fitz.Matrix(8, 8), clip=clip)
out = os.path.join(out_dir, '166_Thein Htaik Soe.jpg')
pix.save(out)
pix.save(os.path.join(workspace, 'crop4_166.jpg'))
doc.close()
print(f'166 zoom8: {os.path.getsize(out)}B  pix={pix.width}x{pix.height}')
