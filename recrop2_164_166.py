import fitz, os

repoDir = r'C:\\Users\\NL－DG　PC1\\Desktop\\Work\\nldg-cv'
pdf_dir = os.path.join(repoDir, 'pdfs')
out_dir = os.path.join(repoDir, 'photos')
workspace = r'C:\\Users\\NL－DG　PC1\\AppData\\Roaming\\Genspark Claw\\users\\74ec096b-b6e9-452b-9a02-f93fbd1489de\\workspace'
zoom = 4

# 164: 枠線内側に絞る（x0を右に、y0を下に、x1を左に、y1を上に）
pdf164 = os.path.join(pdf_dir, '164_Pan Lae Lae Mon.pdf')
doc = fitz.open(pdf164)
page = doc[0]
pw, ph = page.rect.width, page.rect.height
# 前回: x0=0.724 y0=0.088 x1=0.854 y1=0.196  → 枠除去のため内側に5%縮小
clip = fitz.Rect(pw*0.737, ph*0.096, pw*0.845, ph*0.188)
pix = page.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=clip)
out = os.path.join(out_dir, '164_Pan Lae Lae Mon.jpg')
pix.save(out)
pix.save(os.path.join(workspace, 'crop3_164.jpg'))
doc.close()
print(f'164: {os.path.getsize(out)}B')

# 166: 右端の縦線を避けx1を縮小、下部余白を除くy1も縮小
pdf166 = os.path.join(pdf_dir, '166_Thein Htaik Soe.pdf')
doc = fitz.open(pdf166)
page = doc[0]
pw, ph = page.rect.width, page.rect.height
# 前回: x0=0.407 y0=0.096 x1=0.485 y1=0.220 → x1を0.473に、y1を0.205に
clip = fitz.Rect(pw*0.412, ph*0.100, pw*0.473, ph*0.205)
pix = page.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=clip)
out = os.path.join(out_dir, '166_Thein Htaik Soe.jpg')
pix.save(out)
pix.save(os.path.join(workspace, 'crop3_166.jpg'))
doc.close()
print(f'166: {os.path.getsize(out)}B')
